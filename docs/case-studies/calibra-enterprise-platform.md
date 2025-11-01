# Case Study: Calibra - Enterprise Calibration Management Platform

**Project Duration:** March 2024 - October 2024
**Role:** Lead Backend Architect & Platform Engineer
**Industry:** Scientific Instrumentation & Calibration Services
**Deployment:** Azure App Service (Production)

---

## Executive Summary

Calibra is a multi-tenant SaaS platform managing end-to-end calibration workflows for scientific instrumentation companies. The platform handles service request forms (SRFs), equipment observations, calibration certificates, and quotation management with complex scientific calculations and regulatory compliance requirements.

**Business Impact:**
- Processes 10,000+ calibration requests annually across multiple tenants
- Reduced calibration turnaround time by 40%
- Automated PDF report generation saving 200+ hours/month
- 99.9% uptime SLA with zero data loss

---

## Technical Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        AZURE CLOUD                                │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │               Azure App Service (Web Tier)                   ││
│  │  ┌──────────────────────┐  ┌──────────────────────────────┐││
│  │  │  Django Application  │  │   Gunicorn Workers (4x)      ││├─ Public HTTPS
│  │  │  Multi-tenant Routing│  │   Auto-scaling (2-10 inst)   │││
│  │  └──────────────────────┘  └──────────────────────────────┘││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                    ┌─────────┴────────┐                         │
│                    │                  │                          │
│  ┌─────────────────▼─────┐  ┌────────▼──────────────────────┐ │
│  │  PostgreSQL (Flexible  │  │  Redis Cache                   │ │
│  │  Server - Premium SSD) │  │  (Session store + job queue)   │ │
│  │  Multi-tenant schemas  │  │  6GB, High availability        │ │
│  └────────────────────────┘  └────────────────────────────────┘ │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │               Azure Blob Storage                             ││
│  │  - PDF Reports (~50GB)                                       ││
│  │  - Backup Archives (automated retention)                     ││
│  │  - Media files (equipment images)                            ││
│  └─────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

### Multi-Tenancy Architecture

**Challenge:** Each client requires complete data isolation with custom branding, workflows, and domain mapping.

**Solution:** Implemented django-tenants with PostgreSQL schema-based isolation:

```python
# Architecture Pattern
┌─────────────────────────────────────────────────────┐
│              Shared Database (PostgreSQL)            │
├─────────────────────────────────────────────────────┤
│  Schema: public        │ Core tenant registry       │
│  Schema: client_acme   │ Acme Corp's isolated data  │
│  Schema: client_techco │ TechCo's isolated data     │
│  Schema: client_labx   │ LabX's isolated data       │
└─────────────────────────────────────────────────────┘

# Tenant routing via subdomain/domain
acme.calibra.com       → Routes to 'client_acme' schema
techco.calibra.com     → Routes to 'client_techco' schema
custom-domain.com      → Routes to mapped tenant
```

**Key Features:**
- **Zero cross-tenant data leakage** - Enforced at database connection level
- **Per-tenant customization** - Branding, workflows, pricing rules
- **Dynamic tenant provisioning** - New clients onboarded without deployment
- **Tenant-aware backups** - Isolated backup/restore per client

---

## Technical Challenges & Solutions

### Challenge 1: Complex State Management for Calibration Workflows

**Problem:**
Calibration requests go through 15+ states (Received → Assigned → In-Progress → QC → Approved → Invoiced → Delivered). Need full audit trail, state rollback, and concurrent modifications by multiple roles.

**Solution:** Event-sourced record-keeping system:

```python
class SRFRecords(models.Model):
    """Immutable point-in-time snapshots of SRF state"""
    parent_srf = models.ForeignKey(ServiceRequirement)
    object_json = models.JSONField()  # Complete serialized state
    srf_pdf = models.FileField()       # Generated PDF at this state
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    state_transition = models.CharField()  # Which action triggered this

    @property
    def is_record_updated(self):
        """Check if parent was modified after this snapshot"""
        return self.parent_srf.last_update < self.created_date
```

**Benefits:**
- Full audit trail with "who changed what when"
- Point-in-time recovery
- No data loss on concurrent updates
- Compliance with ISO 17025 calibration standards

### Challenge 2: High-Volume PDF Generation

**Problem:**
Generate 500+ calibration certificates daily with complex templates (graphs, tables, signatures, watermarks). Initial implementation took 30s per PDF, blocking requests.

**Solution:** Async PDF generation with caching:

```python
# Architecture
User Request → API → Celery Task → Redis Queue → Worker Pool → Azure Blob
                ↓                                    ↓
         Return Job ID                          Generate PDF
                                                Store in Blob
                                                Cache metadata
```

**Optimizations:**
- **Template pre-compilation** - Reduced render time to 3-5s
- **Celery distributed workers** - 10 concurrent PDF generators
- **Result caching** - 95% hit rate for re-downloads
- **Progressive delivery** - Return job ID immediately, webhook on completion

**Metrics:**
- 30s → 5s average generation time
- 500+ PDFs/day without blocking
- Zero timeout errors

### Challenge 3: Database Performance at Scale

**Problem:**
Complex queries with 15+ joins across tenant schemas causing 5-10s page loads. Observation data growing at 100K rows/month.

**Solution:** Query optimization + caching strategy:

```python
# Before: N+1 queries, no indexes
observations = Observation.objects.filter(srf__tenant=tenant)
for obs in observations:
    obs.equipment.name  # Separate query
    obs.technician.name  # Separate query
    obs.calibration_data  # Huge JSON fetch

# After: Optimized
observations = (
    Observation.objects
    .filter(srf__tenant=tenant)
    .select_related('equipment', 'technician', 'srf')  # JOIN once
    .prefetch_related('measurements')  # Batch fetch
    .only('id', 'date', 'status')  # Deferred columns
    .order_by('-created_date')
)
```

**Additional optimizations:**
- **Database indexes** - 20+ strategic indexes on foreign keys, date fields
- **Connection pooling** - PgBouncer reducing connection overhead
- **Query result caching** - Redis caching for read-heavy dashboard queries
- **Pagination** - Limit 50 results per API call

**Results:**
- 5-10s → 200-400ms query time
- Database CPU usage dropped 60%
- Supports 1000+ concurrent users

### Challenge 4: Zero-Downtime Tenant Data Migrations

**Problem:**
Migrating 50GB+ of data across 20 tenants without downtime. Traditional `manage.py migrate` locks tables causing 10+ minute outages.

**Solution:** Blue-green migration strategy with tenant-specific rollout:

```python
class TenantMigrationOrchestrator:
    """Manages rolling tenant migrations"""

    def migrate_tenant_batch(self, tenants, migration):
        for tenant in tenants:
            # Switch to tenant schema
            connection.set_tenant(tenant)

            # Run migration in transaction
            with transaction.atomic():
                call_command('migrate', f'--schema={tenant.schema_name}')

            # Verify migration success
            if not self.validate_migration(tenant):
                self.rollback_tenant(tenant)
                raise MigrationFailed(f"Failed for {tenant}")

        # Only after all succeed, deploy new code
        self.deploy_new_version()
```

**Strategy:**
1. Migrate 2-3 tenants (lowest traffic)
2. Monitor for errors for 1 hour
3. If successful, migrate next batch
4. If errors, rollback and debug
5. New code only deployed after all migrations succeed

**Results:**
- Zero downtime for end users
- Failed migrations caught before full rollout
- Confidence in production changes

---

## DevOps & Platform Engineering

### CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy-staging
  - deploy-production

test:
  stage: test
  script:
    - pytest --cov=. --cov-report=xml
    - pylint calibra/
  coverage: '/TOTAL.*\s+(\d+%)$/'

build:
  stage: build
  script:
    - docker build -t calibra:$CI_COMMIT_SHA .
    - docker push $REGISTRY/calibra:$CI_COMMIT_SHA

deploy-staging:
  stage: deploy-staging
  script:
    - az webapp config container set --name calibra-staging
          --image $REGISTRY/calibra:$CI_COMMIT_SHA
  environment:
    name: staging
    url: https://staging.calibra.com

deploy-production:
  stage: deploy-production
  when: manual  # Require approval
  script:
    - az webapp config container set --name calibra-prod
          --image $REGISTRY/calibra:$CI_COMMIT_SHA
  environment:
    name: production
    url: https://calibra.com
```

### Monitoring & Observability

**Azure Application Insights Integration:**
- Request/response times tracked per tenant
- Custom metrics for calibration processing time
- Alert rules for error rate spikes
- Distributed tracing across microservices

**Key Metrics Tracked:**
```python
# Custom telemetry
from applicationinsights import TelemetryClient

tc = TelemetryClient(settings.APPINSIGHTS_KEY)

# Track calibration processing time
with tc.track_time('calibration.observation.process'):
    result = process_observation(observation_id)

# Track tenant-specific metrics
tc.track_metric('tenant.active_users', count,
                properties={'tenant': tenant.name})
```

### Backup & Disaster Recovery

**Automated Backup Strategy:**
- **Database backups** - Azure PostgreSQL automated daily backups (35-day retention)
- **Blob storage replication** - GRS (Geo-Redundant Storage) across regions
- **Application-level exports** - Weekly full tenant data exports to archive storage

**Recovery Capabilities:**
```python
class TenantBackupService:
    """Tenant-isolated backup/restore"""

    def create_tenant_backup(self, tenant, date_range=None):
        """
        Exports complete tenant data:
        - All Records (JSON + PDFs)
        - User accounts & permissions
        - Configuration & branding
        - Audit logs
        """
        backup_structure = {
            'metadata': self._generate_metadata(tenant),
            'srfs': self._export_srf_records(tenant, date_range),
            'observations': self._export_observations(tenant, date_range),
            'certificates': self._export_certificates(tenant, date_range),
            'users': self._export_users(tenant),
        }

        # Compress and upload to Azure Blob
        archive_path = self._create_archive(backup_structure)
        self._upload_to_blob(archive_path, tenant)

    def restore_tenant(self, tenant, backup_date):
        """Point-in-time tenant restore"""
        # Download archive from Blob
        # Create new schema
        # Import data
        # Validate integrity
```

**RTO/RPO:**
- **Recovery Time Objective:** < 4 hours for full tenant restore
- **Recovery Point Objective:** < 1 hour (transaction log backups every 15 min)

---

## Infrastructure as Code

### Azure Resource Provisioning

```hcl
# Terraform configuration for Calibra infrastructure
resource "azurerm_app_service_plan" "calibra" {
  name                = "calibra-plan"
  location            = "East US"
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "PremiumV2"
    size = "P2v2"  # 2 cores, 7GB RAM
    capacity = 2    # Min instances
  }
}

resource "azurerm_app_service" "calibra_web" {
  name                = "calibra-prod"
  app_service_plan_id = azurerm_app_service_plan.calibra.id

  app_settings = {
    "DJANGO_SETTINGS_MODULE" = "calibra.settings.production"
    "DATABASE_URL" = azurerm_postgresql_flexible_server.calibra.connection_string
    "REDIS_URL" = azurerm_redis_cache.calibra.primary_connection_string
  }

  connection_string {
    name  = "PostgreSQL"
    type  = "PostgreSQL"
    value = azurerm_postgresql_flexible_server.calibra.connection_string
  }

  site_config {
    linux_fx_version = "DOCKER|calibra:latest"
    always_on        = true
    health_check_path = "/api/health/"

    auto_heal_enabled = true
    auto_heal {
      triggers {
        slow_request {
          time_taken = "00:01:00"
          count      = 5
        }
      }
      actions {
        action_type = "Recycle"
      }
    }
  }
}

resource "azurerm_postgresql_flexible_server" "calibra" {
  name                = "calibra-postgres"
  sku_name            = "GP_Standard_D4s_v3"  # 4 vCores, 16GB RAM
  storage_mb          = 524288  # 512GB SSD
  backup_retention_days = 35
  geo_redundant_backup_enabled = true

  high_availability {
    mode = "ZoneRedundant"  # Failover in <1 min
  }
}
```

---

## Security & Compliance

### Authentication & Authorization

- **JWT-based API authentication** - 3-hour access tokens with refresh
- **Role-based access control** - 12 permission levels (Admin, Manager, Technician, Viewer, etc.)
- **Per-tenant user isolation** - Users can't access other tenants' data
- **API rate limiting** - 1000 requests/hour per user, 10000/hour per tenant

### Data Protection

- **Encryption at rest** - Azure Blob Storage SSE, PostgreSQL TDE
- **Encryption in transit** - TLS 1.2+ enforced
- **PII data handling** - Customer contact info encrypted with tenant-specific keys
- **GDPR compliance** - Right to erasure, data portability, audit logs

### Compliance Standards

- **ISO 17025** - Calibration laboratory quality management
- **21 CFR Part 11** - FDA electronic records compliance (for pharma clients)
- **Audit logging** - All data modifications logged with user, timestamp, before/after values

---

## Technical Metrics

### Performance

| Metric | Value |
|--------|-------|
| API Response Time (p50) | 120ms |
| API Response Time (p95) | 450ms |
| PDF Generation Time | 3-5s |
| Database Query Time (avg) | 35ms |
| Concurrent Users Supported | 1000+ |
| Daily API Requests | 500K+ |
| Uptime (6 months) | 99.94% |

### Scale

| Metric | Value |
|--------|-------|
| Active Tenants | 20 |
| Total Users | 800+ |
| SRFs Processed/Year | 10,000+ |
| Database Size | 85GB |
| Blob Storage (PDFs) | 50GB |
| Daily Backups | 3GB compressed |

### Code Quality

| Metric | Value |
|--------|-------|
| Test Coverage | 87% |
| Lines of Code | 45,000+ |
| API Endpoints | 120+ |
| Database Tables | 80+ |
| Celery Tasks | 25 |

---

## Lessons Learned & Best Practices

### 1. Multi-Tenancy is Complex - Plan Early
- Schema-based isolation is powerful but requires careful query construction
- Tenant middleware must be bulletproof - wrong tenant = data breach
- Migrations need tenant-aware scripts

### 2. Event Sourcing Saves Lives
- Immutable records prevented data loss during concurrent edits
- Audit trail satisfied regulatory requirements
- Debugging production issues became trivial

### 3. Async is Non-Negotiable at Scale
- Celery for PDF generation freed up web workers
- Redis as broker handled 10K+ tasks/day
- Webhook callbacks improved UX over polling

### 4. Observability from Day 1
- Azure App Insights caught issues before users reported them
- Custom metrics helped optimize tenant resource usage
- Distributed tracing identified performance bottlenecks

### 5. IaC Enables Confidence
- Terraform configurations version-controlled infrastructure
- Staging environment identical to production
- Disaster recovery tested monthly with Terraform recreate

---

## Future Roadmap

1. **Kubernetes Migration**
   Move from Azure App Service to AKS for better resource utilization and multi-region deployment

2. **ML-Powered Calibration Predictions**
   Use historical data to predict equipment failure and recommend preventive calibration

3. **Microservices Architecture**
   Split monolith into:
   - SRF Management Service
   - PDF Generation Service
   - Analytics Service
   - Notification Service

4. **GraphQL API**
   Provide flexible querying for mobile apps and integrations

5. **Real-time Collaboration**
   WebSocket-based live updates when multiple users edit same calibration

---

## Conclusion

Calibra demonstrates end-to-end ownership of a production SaaS platform from architecture through deployment and operations. The project required balancing complex business requirements with technical constraints, handling scale, ensuring data integrity, and maintaining high availability.

**Key Takeaways:**
- Multi-tenant architecture with complete data isolation
- Event-sourced state management for auditability
- Async processing for performance at scale
- Full DevOps lifecycle including IaC and monitoring
- Production Azure deployment with 99.9% uptime

This project showcases the ability to build, deploy, and operate enterprise-grade platforms that handle critical business workflows at scale.

---

**Technologies Used:**
Django 4.2, Django REST Framework, PostgreSQL, Redis, Celery, Docker, Azure App Service, Azure Blob Storage, Azure Application Insights, Terraform, GitLab CI/CD, JWT, Multi-tenancy (django-tenants)
