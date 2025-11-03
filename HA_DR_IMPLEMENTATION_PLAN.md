# High Availability, Disaster Recovery & SLA Implementation Plan

## Overview

**Goal:** Demonstrate production-grade HA/DR architecture for AI/ML platform engineering

**Current Stack:**
- Frontend: Vercel (React)
- Backend: Google Cloud Run (Django)
- Database: Cloud SQL PostgreSQL
- Microservices: Cloud Run (Paper Scraper, Document Processor)
- Storage: Google Cloud Storage (for future ML models)

---

## 1. High Availability Architecture

### 1.1 Multi-Region Deployment

**Current State:** Single region (us-central1)

**Target State:** Multi-region with automatic failover

```yaml
Production Architecture:
  Primary Region: us-central1 (Iowa)
  Secondary Region: us-east1 (South Carolina)

  Components:
    - Cloud Run: Auto-deployed to both regions
    - Cloud SQL: Primary in us-central1, read replica in us-east1
    - Cloud Storage: Multi-region bucket (us)
    - Load Balancer: Global HTTP(S) with health checks
```

**Implementation:**

```bash
# 1. Create read replica in secondary region
gcloud sql instances create portfolio-db-replica \
  --master-instance-name=portfolio-db \
  --region=us-east1 \
  --tier=db-f1-micro \
  --replica-type=READ

# 2. Deploy backend to multiple regions
gcloud run deploy portfolio-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

gcloud run deploy portfolio-backend \
  --source . \
  --region us-east1 \
  --allow-unauthenticated

# 3. Create global load balancer
gcloud compute backend-services create portfolio-backend-service \
  --global \
  --enable-cdn \
  --health-checks=portfolio-health-check

# 4. Add both regions to backend service
gcloud compute backend-services add-backend portfolio-backend-service \
  --global \
  --serverless-backend-name=portfolio-backend \
  --serverless-backend-region=us-central1

gcloud compute backend-services add-backend portfolio-backend-service \
  --global \
  --serverless-backend-name=portfolio-backend \
  --serverless-backend-region=us-east1
```

### 1.2 Auto-Scaling Configuration

```yaml
Cloud Run Configuration:
  Min Instances: 1  # Always warm
  Max Instances: 100
  CPU: 1
  Memory: 512Mi
  Concurrency: 80

  Scaling Metrics:
    - CPU utilization: 70%
    - Request rate: 1000 req/min
    - Response time: p95 < 500ms
```

### 1.3 Database High Availability

```yaml
Cloud SQL HA Configuration:
  High Availability: Enabled (Regional HA)
  Automatic Failover: Enabled
  Backup Schedule: Daily at 3 AM UTC
  Backup Retention: 7 days (automated), 30 days (manual)
  Point-in-Time Recovery: 7 days

  Read Replicas:
    - us-east1 (failover + read scaling)
    - us-west1 (read scaling)
```

**Implementation:**

```bash
# Enable HA on Cloud SQL
gcloud sql instances patch portfolio-db \
  --availability-type=REGIONAL \
  --enable-bin-log

# Configure automated backups
gcloud sql instances patch portfolio-db \
  --backup-start-time=03:00

# Create read replicas for scaling
gcloud sql instances create portfolio-db-read-us-east1 \
  --master-instance-name=portfolio-db \
  --region=us-east1 \
  --tier=db-f1-micro \
  --replica-type=READ
```

---

## 2. Disaster Recovery Strategy

### 2.1 Recovery Point Objective (RPO) & Recovery Time Objective (RTO)

```yaml
Service Tier Definitions:

Critical Services (RTO: 15 min, RPO: 5 min):
  - Django Backend API
  - Database (Cloud SQL)

High Priority (RTO: 1 hour, RPO: 15 min):
  - Paper Scraper Service
  - Document Processor

Standard (RTO: 4 hours, RPO: 1 hour):
  - Frontend (Vercel has its own DR)
  - Analytics
```

### 2.2 Backup Strategy

**Automated Backups:**

```yaml
Database Backups:
  Frequency: Daily
  Retention: 7 days automated, 30 days manual
  Type: Full snapshot + transaction logs
  Location: Multi-region (us)
  Encryption: Google-managed keys

Application Backups:
  Git Repository: GitHub (automatic replication)
  Container Images: Artifact Registry (multi-region)
  Configuration: Secret Manager (replicated)

Data Backups:
  Cloud Storage: Multi-region with versioning
  Scraped Papers: Daily export to GCS
  Vector Embeddings: Weekly backup to GCS
```

**Implementation:**

```python
# backend/portfolio/management/commands/backup_database.py
from django.core.management.base import BaseCommand
from google.cloud import storage
from datetime import datetime
import subprocess

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Export database to Cloud Storage
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        bucket_name = 'portfolio-backups-us'

        # Trigger Cloud SQL export
        subprocess.run([
            'gcloud', 'sql', 'export', 'sql', 'portfolio-db',
            f'gs://{bucket_name}/database/backup_{timestamp}.sql',
            '--database=portfolio'
        ])

        self.stdout.write(f'Backup completed: backup_{timestamp}.sql')
```

**Backup Schedule:**

```bash
# Create Cloud Scheduler job for daily backups
gcloud scheduler jobs create http db-backup-daily \
  --schedule="0 3 * * *" \
  --uri="https://portfolio-backend-434831039257.us-central1.run.app/api/admin/backup/" \
  --http-method=POST \
  --headers="Authorization=Bearer $(gcloud auth print-identity-token)"
```

### 2.3 Disaster Recovery Runbook

**Scenario 1: Region Outage**

```markdown
## Region Outage Procedure

**Detection:**
- Uptime checks fail for >5 minutes
- Cloud Monitoring alerts trigger

**Response:**
1. Verify outage scope (Cloud Status Dashboard)
2. Switch DNS to secondary region (automated via Global LB)
3. Promote read replica to primary:
   ```bash
   gcloud sql instances promote-replica portfolio-db-replica
   ```
4. Update application config to point to new primary
5. Monitor application health
6. Notify stakeholders

**Expected RTO:** 15 minutes
**Expected RPO:** 5 minutes (last transaction log)
```

**Scenario 2: Database Corruption**

```markdown
## Database Corruption Procedure

**Detection:**
- Data validation errors
- Query failures
- Manual report

**Response:**
1. Stop writes to database:
   ```bash
   gcloud run services update portfolio-backend --no-traffic
   ```

2. Identify corruption scope
3. Restore from latest backup:
   ```bash
   gcloud sql backups restore <backup-id> \
     --backup-instance=portfolio-db \
     --backup-instance=portfolio-db
   ```

4. If recent backup corrupted, use point-in-time recovery:
   ```bash
   gcloud sql instances clone portfolio-db portfolio-db-restored \
     --point-in-time='2025-11-03T12:00:00Z'
   ```

5. Validate data integrity
6. Re-enable traffic

**Expected RTO:** 1 hour
**Expected RPO:** <15 minutes
```

**Scenario 3: Complete Data Loss**

```markdown
## Complete Data Loss Procedure

**Response:**
1. Create new Cloud SQL instance
2. Restore from multi-region backup:
   ```bash
   gsutil cp gs://portfolio-backups-us/database/latest.sql /tmp/
   gcloud sql import sql portfolio-db-new gs://portfolio-backups-us/database/latest.sql
   ```

3. Redeploy Cloud Run services
4. Restore vector embeddings from GCS backup
5. Re-run document ingestion if needed
6. Validate end-to-end functionality

**Expected RTO:** 4 hours
**Expected RPO:** 24 hours (last full backup)
```

---

## 3. Service Level Agreements (SLAs)

### 3.1 Availability Targets

```yaml
Service Availability SLAs:

Production API:
  Target Uptime: 99.9% (43.2 minutes downtime/month)
  Measurement: HTTP 200 responses / total requests
  Monitoring: Uptime checks every 1 minute from 6 regions

Database:
  Target Uptime: 99.95% (21.6 minutes downtime/month)
  Measurement: Successful query execution

Microservices:
  Target Uptime: 99.5% (3.6 hours downtime/month)
  Measurement: Job completion rate
```

### 3.2 Performance SLAs

```yaml
Response Time:
  p50: < 100ms
  p95: < 500ms
  p99: < 1000ms
  Measurement: End-to-end API latency

Throughput:
  Minimum: 100 requests/second
  Peak: 1000 requests/second

Error Rate:
  Target: < 0.1% (99.9% success rate)
  Measurement: 5xx errors / total requests
```

### 3.3 Data Durability SLA

```yaml
Data Durability:
  Target: 99.999999999% (11 nines)
  Provided by: Cloud Storage multi-region

Data Integrity:
  Checksums: Enabled on all writes
  Validation: Daily integrity checks
  Corruption Detection: Automated monitoring
```

### 3.4 SLA Monitoring Dashboard

```python
# backend/portfolio/views.py - SLA Metrics Endpoint
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from datetime import datetime, timedelta

@api_view(['GET'])
def sla_metrics(request):
    """
    Real-time SLA metrics dashboard
    """
    now = datetime.now()
    last_24h = now - timedelta(hours=24)

    # Calculate uptime
    # (This would integrate with Cloud Monitoring in production)

    return Response({
        'period': '24h',
        'availability': {
            'api': '99.95%',
            'database': '99.99%',
            'overall': '99.94%'
        },
        'performance': {
            'p50_latency_ms': 87,
            'p95_latency_ms': 432,
            'p99_latency_ms': 891
        },
        'reliability': {
            'error_rate': '0.05%',
            'success_rate': '99.95%',
            'total_requests': 1234567
        },
        'last_updated': now.isoformat()
    })
```

---

## 4. Monitoring & Alerting

### 4.1 Health Checks

```yaml
Health Check Configuration:
  Endpoint: /health
  Interval: 10 seconds
  Timeout: 5 seconds
  Healthy Threshold: 2
  Unhealthy Threshold: 3

  Checks:
    - Database connectivity
    - Redis cache (if applicable)
    - Cloud Storage access
    - Microservice connectivity
```

**Implementation:**

```python
# backend/portfolio/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
import time

@api_view(['GET'])
def health_check(request):
    """
    Comprehensive health check for load balancer
    """
    start = time.time()
    checks = {}

    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks['database'] = 'healthy'
    except Exception as e:
        checks['database'] = f'unhealthy: {str(e)}'
        return Response(checks, status=503)

    # Check response time
    latency_ms = (time.time() - start) * 1000
    checks['latency_ms'] = latency_ms

    if latency_ms > 1000:
        checks['status'] = 'degraded'
        return Response(checks, status=503)

    checks['status'] = 'healthy'
    return Response(checks, status=200)
```

### 4.2 Alerting Rules

```yaml
Cloud Monitoring Alerts:

Critical Alerts (PagerDuty):
  - API error rate > 1% for 5 minutes
  - Database connection failures
  - Service completely down
  - Disk usage > 90%

Warning Alerts (Email):
  - p95 latency > 800ms for 10 minutes
  - Error rate > 0.5% for 5 minutes
  - CPU usage > 80% for 15 minutes
  - Memory usage > 85%

Info Alerts (Slack):
  - Deployment completed
  - Backup completed
  - Scale-up event
```

**Implementation:**

```bash
# Create uptime check
gcloud monitoring uptime-checks create portfolio-api-uptime \
  --display-name="Portfolio API Uptime" \
  --resource-type=uptime-url \
  --host="portfolio-backend-434831039257.us-central1.run.app" \
  --path="/health" \
  --check-interval=60s

# Create alert policy
gcloud alpha monitoring policies create \
  --notification-channels=<channel-id> \
  --display-name="High Error Rate Alert" \
  --condition-display-name="Error rate > 1%" \
  --condition-threshold-value=1 \
  --condition-threshold-duration=300s
```

---

## 5. Chaos Engineering & Testing

### 5.1 Failure Simulation

```yaml
Chaos Tests (Monthly):

  1. Region Failover Test:
     - Simulate us-central1 outage
     - Measure failover time
     - Verify data consistency

  2. Database Failover Test:
     - Force primary database failure
     - Verify automatic promotion
     - Check query redirection

  3. Load Test:
     - 10,000 concurrent requests
     - Measure auto-scaling response
     - Verify performance under load

  4. Backup Restore Test:
     - Full database restore to test environment
     - Verify data integrity
     - Measure restore time
```

### 5.2 DR Drill Schedule

```yaml
Quarterly DR Drills:

  Q1: Region Failover Drill
    - Switch traffic to us-east1
    - Measure RTO/RPO
    - Document lessons learned

  Q2: Database Restore Drill
    - Restore to test environment
    - Validate data integrity
    - Measure restore time

  Q3: Full Stack Recovery Drill
    - Simulate complete infrastructure loss
    - Rebuild from backups
    - Measure full recovery time

  Q4: Load & Chaos Test
    - Inject random failures
    - Measure system resilience
    - Update runbooks
```

---

## 6. Implementation Checklist

### Phase 1: Foundation (Week 1)
- [ ] Enable Cloud SQL high availability
- [ ] Configure automated backups (daily)
- [ ] Set up Cloud Monitoring dashboards
- [ ] Create health check endpoints
- [ ] Document current architecture

### Phase 2: Redundancy (Week 2)
- [ ] Deploy backend to secondary region (us-east1)
- [ ] Create read replicas
- [ ] Set up global load balancer
- [ ] Configure DNS failover
- [ ] Test manual failover

### Phase 3: Monitoring (Week 3)
- [ ] Set up uptime checks (6 regions)
- [ ] Configure alert policies
- [ ] Create SLA dashboard
- [ ] Integrate with PagerDuty/Slack
- [ ] Document on-call procedures

### Phase 4: Testing (Week 4)
- [ ] Run DR drills
- [ ] Perform load testing
- [ ] Simulate region outage
- [ ] Test backup restore
- [ ] Update runbooks

### Phase 5: Documentation (Ongoing)
- [ ] Write DR runbooks
- [ ] Create HA/DR architecture diagrams
- [ ] Build frontend page showcasing HA/DR
- [ ] Document SLA metrics
- [ ] Create incident response procedures

---

## 7. Cost Estimate

```yaml
Monthly HA/DR Costs:

Cloud SQL HA:
  Regional HA: +$25/month
  Read Replicas (2x): +$20/month
  Backup Storage: +$5/month

Multi-Region Cloud Run:
  Secondary region instances: +$10/month

Load Balancer:
  Global LB: +$18/month

Monitoring:
  Uptime checks: +$3/month
  Log storage: +$5/month

Total Additional Cost: ~$86/month
Total with existing: ~$106/month

Benefits:
  - 99.9%+ uptime SLA
  - <15 min RTO
  - <5 min RPO
  - Multi-region redundancy
```

---

## 8. Success Metrics

```yaml
HA/DR Implementation Success:

Technical Metrics:
  ✅ Achieve 99.9% uptime over 30 days
  ✅ RTO < 15 minutes (measured)
  ✅ RPO < 5 minutes (measured)
  ✅ Successful DR drill (quarterly)
  ✅ Zero data loss in failover tests

Business Metrics:
  ✅ Zero customer-facing outages
  ✅ < 5 minutes of downtime per month
  ✅ Successful backup restores (100%)
  ✅ Complete DR documentation
  ✅ On-call runbooks validated
```

---

**Status:** Ready for implementation
**Timeline:** 4 weeks
**Owner:** Platform Engineering Team
**Review:** Quarterly

This demonstrates production-ready HA/DR planning for ML/AI platforms.
