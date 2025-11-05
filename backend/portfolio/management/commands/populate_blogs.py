"""
Management command to populate the database with technical blog posts
Based on portfolio documentation and case studies
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from portfolio.models import Paper


class Command(BaseCommand):
    help = 'Populate database with technical blog posts from portfolio content'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Populating blog posts...'))

        # Clear existing posts first
        Paper.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing blog posts'))

        blog_posts = [
            {
                'title': 'Building Production-Ready Kubernetes Deployments on Azure AKS',
                'abstract': '''Deploying applications to Kubernetes can seem daunting, but with the right approach, it becomes manageable and even enjoyable. In this post, I'll walk through my experience deploying a Django-based Learning Management System to Azure Kubernetes Service (AKS).

**The Challenge**

I had a multi-component Django application (web server, Celery workers, Celery Beat scheduler, PostgreSQL, and Redis) that needed to scale efficiently and maintain high availability. The application handles user sessions, background PDF generation, and scheduled tasks.

**Architecture Decisions**

I chose Kubernetes for its powerful orchestration capabilities and AKS for its managed control plane and seamless integration with Azure services. The architecture includes:

- **StatefulSet for PostgreSQL**: Ensures stable network identity and persistent storage using Azure Managed Disks (20GB with ReadWriteOnce access mode)
- **Deployment for Django**: Runs 3 replicas by default with Horizontal Pod Autoscaling (HPA) configured to scale up to 10 pods based on CPU (70%) and memory (75%) utilization
- **Deployment for Celery Workers**: Starts with 2 replicas and autoscales to 6 based on workload
- **Deployment for Celery Beat**: Single replica (singleton) using Recreate strategy to prevent duplicate scheduled tasks
- **Deployment for Redis**: Single replica with 5GB persistent storage and AOF persistence

**Implementation Highlights**

Init Containers were crucial for proper startup sequencing. Before the Django pods start serving traffic, init containers ensure:
- PostgreSQL is accepting connections (wait-for-db)
- Redis is responding to ping (wait-for-redis)
- Database migrations are applied (migrate)
- Static files are collected to Azure Files shared storage (collectstatic)

Health checks prevent traffic from reaching unhealthy pods. I configured liveness probes (restart if failing) and readiness probes (remove from load balancer if failing) for all components.

**Storage Strategy**

Azure Files (RWX - ReadWriteMany) for shared media and static files allows multiple Django pods to read/write the same files. Azure Managed Disks (RWO - ReadWriteOnce) for PostgreSQL and Redis provides high-performance block storage.

**Autoscaling Configuration**

The HPA configuration uses careful stabilization windows to prevent flapping:
- Scale up policy: Fast (doubles pods every 30 seconds during spike)
- Scale down policy: Slow (reduces 50% after 5 minutes of low usage)

This ensures quick response to traffic spikes while avoiding premature scale-down during temporary lulls.

**Lessons Learned**

1. Always set resource requests AND limits to prevent resource contention
2. Use init containers for dependencies - never assume startup order
3. Implement proper health checks on meaningful endpoints
4. Test autoscaling with realistic load before production
5. Use Azure Files for shared storage needs, not NFS on VMs

**Results**

The deployment now handles 5000+ concurrent users with sub-500ms response times, automatically scales during peak hours, and maintains zero downtime during deployments through rolling updates.

All Kubernetes manifests and Terraform modules are available on my GitHub. Feel free to adapt them for your own deployments!''',
                'authors': 'Vasu Kapoor',
                'source': 'blog',
                'source_id': 'kubernetes-aks-production-deployment',
                'url': None,
                'github_url': 'https://github.com/dreamvasu/ai-platform-portfolio',
                'published_date': (datetime.now() - timedelta(days=2)).date(),
                'category': 'mlops',
                'tags': ['Kubernetes', 'Azure AKS', 'Docker', 'DevOps', 'Platform Engineering', 'Autoscaling'],
                'citation_count': 0,
                'relevance_score': 0.95,
                'is_featured': True
            },
            {
                'title': 'Implementing RAG Systems with Google Vertex AI and ChromaDB',
                'abstract': '''Retrieval-Augmented Generation (RAG) is transforming how we build AI applications. Instead of relying solely on an LLM's training data, RAG systems retrieve relevant context from your own documents before generating responses. Here's how I built a production RAG system.

**Why RAG?**

I needed an AI chatbot that could answer questions about my technical portfolio documentation with high accuracy. Fine-tuning an LLM would be expensive and require retraining for every update. RAG solves this by:
- Querying a vector database for relevant document chunks
- Injecting those chunks as context into the LLM prompt
- Getting accurate, up-to-date answers without retraining

**Technology Stack**

- **Embedding Model**: Google Vertex AI textembedding-gecko@003 (768-dimensional embeddings)
- **Vector Database**: ChromaDB (open-source, Python-native)
- **LLM**: Vertex AI Gemini Pro for response generation
- **Backend**: Django REST Framework
- **Frontend**: React widget with TypeScript

**Document Ingestion Pipeline**

The ingestion process transforms markdown files into searchable embeddings:

1. **Load Documents**: Recursively scan docs/, CLAUDE.md, README.md, etc.
2. **Chunk Text**: Split documents into ~500-word chunks with 100-word overlap to maintain context at boundaries
3. **Generate Embeddings**: Call Vertex AI embedding API (batch processing for efficiency)
4. **Store in ChromaDB**: Save embeddings with metadata (source file, category, chunk ID)

**Query Pipeline**

When a user asks a question:

1. **Embed Query**: Generate embedding vector for the user's question
2. **Similarity Search**: ChromaDB finds top-K most similar document chunks using cosine similarity
3. **Construct Prompt**: Inject retrieved chunks as context
4. **Generate Answer**: Send prompt to Gemini Pro
5. **Return Response**: Include source citations for transparency

**Optimization Strategies**

Chunk Size Tuning: I tested 300, 500, and 700-word chunks. 500 words hit the sweet spot - enough context without diluting relevance.

Overlap is Essential: 100-word overlap between chunks prevents information loss at boundaries. Without it, answers spanning chunk boundaries were incomplete.

Relevance Threshold: Only include chunks with similarity > 0.7. Including low-relevance chunks added noise and reduced answer quality.

Caching: ChromaDB collection is loaded once at startup and kept in memory. Loading on every query added 2-3 seconds latency.

**Real-World Performance**

- Query latency: <200ms (embedding) + ~500ms (Gemini Pro) = ~700ms total
- Accuracy: 85%+ based on manual testing across 50+ questions
- Context relevance: 92% of retrieved chunks were actually relevant to answers

**Cost Analysis**

- Embeddings: ~$0.01 per 1000 chunks (one-time ingestion cost)
- Gemini Pro queries: ~$0.002 per query
- ChromaDB: Free (self-hosted)

For a portfolio chatbot with ~100 queries/month, total cost is negligible (<$1/month).

**Key Takeaways**

1. Start with simple chunking strategies before complex hierarchical methods
2. Tune chunk size based on your document structure
3. Always include source citations for trust and debugging
4. Monitor embedding quality with similarity score distributions
5. Cache embeddings - never re-embed the same content

RAG is incredibly powerful for domain-specific Q&A. The system now handles questions about my Kubernetes deployments, Terraform modules, and technical approaches with impressive accuracy.''',
                'authors': 'Vasu Kapoor',
                'source': 'blog',
                'source_id': 'rag-vertex-ai-chromadb',
                'url': None,
                'github_url': 'https://github.com/dreamvasu/ai-platform-portfolio',
                'published_date': (datetime.now() - timedelta(days=5)).date(),
                'category': 'rag',
                'tags': ['RAG', 'LLM', 'Vertex AI', 'Embeddings', 'ChromaDB', 'Django', 'GCP'],
                'citation_count': 0,
                'relevance_score': 0.98,
                'is_featured': True
            },
            {
                'title': 'Multi-Tenant SaaS Architecture: PostgreSQL Schema Isolation',
                'abstract': '''Building a multi-tenant SaaS application requires careful architectural decisions to ensure data isolation, security, and scalability. I implemented schema-based isolation for Calibra, a calibration management platform serving 20+ enterprise customers.

**Isolation Strategies Compared**

There are three main approaches:

1. **Row-Level**: Single database, single schema, tenant_id column. Simplest but highest risk of data leaks.
2. **Database-Level**: Separate database per tenant. Maximum isolation but difficult to manage at scale.
3. **Schema-Level**: Single database, separate schema per tenant. Best balance of isolation and manageability.

I chose schema-level isolation for Calibra.

**Implementation with django-tenants**

Django doesn't natively support multi-tenancy, but django-tenants provides excellent schema-based isolation:

- Automatic tenant routing based on subdomain (customer1.calibra.com → customer1 schema)
- Transparent query filtering - developers write normal queries, the library handles schema switching
- Safe migrations - apply schema changes to all tenants with a single command

**Tenant Provisioning Flow**

When a new customer signs up:

1. Create tenant record in public schema
2. Create dedicated PostgreSQL schema
3. Run migrations on new schema
4. Provision subdomain (customer.calibra.com)
5. Send welcome email with login URL

This entire flow is automated and takes ~30 seconds.

**Database Design**

The public schema contains:
- Tenant metadata (company name, subdomain, subscription plan)
- Global admin users
- Cross-tenant analytics tables

Each tenant schema contains:
- Customer-specific data (users, calibrations, certificates)
- Complete isolation - no cross-tenant queries possible
- Independent schema versions (for staged rollouts)

**Backup and Recovery**

PostgreSQL pg_dump supports schema-specific backups:

- Daily full backup of public schema
- Daily incremental backups per tenant schema
- Point-in-time recovery per tenant
- Tenant-specific restore without affecting others

**Performance Considerations**

With 20+ tenants in a single database, I monitored:

- Connection pooling: PgBouncer with 100 max connections
- Query performance: Per-schema indexes maintain speed
- Storage: Tablespaces allow distributing tenant data across disks
- Monitoring: pg_stat_statements tracks slow queries per schema

**Security Benefits**

Schema isolation provides strong security:

- SQL injection cannot access other tenants (schema context is set at connection level)
- Accidental queries without tenant context fail fast
- Database user permissions enforced at schema level
- Audit logs track all cross-schema access attempts

**Scaling Challenges**

At 500+ tenants, schema-based isolation hits limits:

- PostgreSQL metadata grows (system catalog overhead)
- Migrations take longer (run on every schema)
- Backup/restore complexity increases

For extreme scale (1000+ tenants), I'd migrate to database-per-tenant with a service mesh for management.

**Production Stats**

Calibra currently serves:
- 22 enterprise customers
- ~500,000 API requests/day
- Average query time <50ms
- Zero cross-tenant data leaks (verified through security audits)

**Lessons Learned**

1. Test tenant isolation with security audits, not just code review
2. Automate all tenant operations (creation, migration, backup)
3. Build admin tooling for cross-tenant analytics from day one
4. Monitor per-tenant resource usage to detect abusive behavior
5. Plan migration strategy before hitting 500 tenants

Schema-based isolation provided the perfect balance for Calibra's scale and security requirements. Would I choose it again? Absolutely.''',
                'authors': 'Vasu Kapoor',
                'source': 'blog',
                'source_id': 'multi-tenant-saas-postgresql',
                'url': None,
                'published_date': (datetime.now() - timedelta(days=8)).date(),
                'category': 'mlops',
                'tags': ['Multi-tenancy', 'SaaS', 'PostgreSQL', 'Django', 'Architecture', 'Security'],
                'citation_count': 0,
                'relevance_score': 0.92,
                'is_featured': True
            },
            {
                'title': 'Infrastructure as Code: Terraform Modules for Multi-Cloud Deployments',
                'abstract': '''Terraform transformed how I manage infrastructure. Instead of clicking through cloud consoles, I now define infrastructure in code, version it in Git, and deploy reproducibly. Here's how I built reusable Terraform modules.

**Why Terraform Modules?**

Without modules, Terraform configurations become repetitive nightmares. Modules provide:
- Reusability across environments (dev/staging/prod)
- Encapsulation of best practices
- Easier testing and validation
- Simplified collaboration

**Module Structure**

I built four core modules for Azure AKS deployment:

1. **Networking Module**: VNet, subnets, NSGs, service endpoints
2. **AKS Cluster Module**: Kubernetes cluster with dual node pools
3. **ACR Module**: Container registry with monitoring
4. **Storage Module**: Azure Files shares and blob containers

Each module has three files:
- `main.tf`: Resource definitions
- `variables.tf`: Input parameters with validation
- `outputs.tf`: Values to pass to other modules

**Networking Module Design**

The networking module creates:
- VNet with configurable address space (default: 10.0.0.0/16)
- AKS subnet (10.0.1.0/24) with service endpoints
- PostgreSQL subnet (10.0.2.0/24) with delegation
- NSG with allow rules for PostgreSQL port

Key feature: Subnet delegation for Azure Database for PostgreSQL enables private connectivity without exposing databases to the internet.

**AKS Cluster Module**

This module provisions:
- System node pool (2-3 nodes, Standard_DS2_v2)
- User node pool (1-5 nodes, autoscaling enabled)
- System-assigned managed identity
- Log Analytics integration
- Auto-upgrade channel (patch)
- Maintenance window (Sundays 2-4 AM)

Variable validation ensures:
- Node counts within limits
- VM sizes are appropriate
- Kubernetes version is supported

**State Management**

Remote state is critical for team collaboration:

- Backend: Azure Storage Account (with versioning)
- State locking: Prevents concurrent modifications
- Encryption: State contains sensitive data (passwords, keys)
- Workspace strategy: One workspace per environment

**Environment Configuration**

Instead of duplicating code, I use environment-specific tfvars:

`terraform/environments/prod/terraform.tfvars`:
```hcl
resource_group_name = "portfolio-prod-rg"
location = "East US"
aks_node_count = 3
enable_autoscaling = true
```

This allows identical module code across all environments with different parameters.

**Cost Optimization Tricks**

1. Use B-series VMs for dev environments
2. Enable cluster autoscaler to scale to zero after hours
3. Use Azure Reserved Instances for prod (34% savings)
4. Implement lifecycle policies for storage (Hot → Cool → Archive)

**Deployment Workflow**

1. Make infrastructure changes in feature branch
2. Run `terraform plan` in CI/CD pipeline
3. Review plan output in PR comments
4. Merge PR to apply changes automatically
5. Terraform runs in pipeline with approval gate

**Module Reusability**

These modules work across projects:
- Deployed Ringlet LMS to AKS
- Deployed ML training platform
- Deployed internal developer tools

Each project uses the same modules with different variables. When I improve a module, all projects benefit.

**Terraform vs Alternatives**

I chose Terraform over:
- ARM templates: Too verbose, Azure-only
- Pulumi: Prefer HCL over programming languages
- CDK for Terraform: Extra abstraction layer unnecessary

Terraform's declarative syntax and broad provider support made it ideal.

**Lessons Learned**

1. Start with modules from day one - refactoring later is painful
2. Version modules (semantic versioning in Git tags)
3. Test modules with terraform-compliance
4. Document every variable with description and validation
5. Use count/for_each sparingly - readability matters

My Terraform modules now provision production infrastructure in 20 minutes. The same infrastructure manually configured would take 4-6 hours and include inconsistencies.''',
                'authors': 'Vasu Kapoor',
                'source': 'blog',
                'source_id': 'terraform-iac-modules',
                'url': None,
                'github_url': 'https://github.com/dreamvasu/ai-platform-portfolio',
                'published_date': (datetime.now() - timedelta(days=10)).date(),
                'category': 'mlops',
                'tags': ['Terraform', 'IaC', 'Azure', 'GCP', 'DevOps', 'Cloud Infrastructure'],
                'citation_count': 0,
                'relevance_score': 0.90,
                'is_featured': False
            },
            {
                'title': 'Kubernetes Horizontal Pod Autoscaling: From 3 to 10 Pods in 30 Seconds',
                'abstract': '''Horizontal Pod Autoscaling (HPA) is Kubernetes' answer to traffic spikes. When configured correctly, it seamlessly scales your application to handle load. When configured poorly, it causes flapping, over-provisioning, and instability.

**The Problem**

My Django application ran 3 pods handling normal traffic (500-1000 concurrent users). During marketing campaigns, traffic spiked 5x within minutes. Manual scaling was too slow and required on-call intervention.

**HPA Configuration**

Kubernetes HPA watches metrics and adjusts replica count to maintain targets. My configuration:

```yaml
minReplicas: 3
maxReplicas: 10
metrics:
- type: Resource
  resource:
    name: cpu
    target:
      type: Utilization
      averageUtilization: 70
- type: Resource
  resource:
    name: memory
    target:
      type: Utilization
      averageUtilization: 75
```

**Why These Targets?**

CPU 70%: Higher threshold (like 90%) risks pod crashes during sudden spikes. Lower threshold (like 50%) wastes resources.

Memory 75%: Memory usage changes more slowly than CPU. 75% provides buffer before OOM kills.

Multiple Metrics: HPA scales based on whichever metric is highest, ensuring responsiveness to different bottlenecks.

**Preventing Flapping**

Without stabilization, HPA can cause flapping:
- Traffic spike → Scale up to 10 pods
- Traffic drops → Scale down to 3 pods
- Traffic spike → Scale up again
- Repeat (cluster chaos)

Stabilization windows prevent this:

Scale Up Behavior:
- Policy: 100% increase (double pods)
- Stabilization: 30 seconds
- Result: Fast scale up during spikes

Scale Down Behavior:
- Policy: 50% decrease (remove half of pods)
- Stabilization: 5 minutes
- Result: Slow scale down prevents premature reduction

**Resource Requests and Limits**

HPA calculates percentage based on resource requests:

```yaml
resources:
  requests:
    cpu: 250m
    memory: 512Mi
  limits:
    cpu: 500m
    memory: 1Gi
```

If requests are too low, HPA won't scale enough. Too high, and you waste money on over-provisioned nodes.

**Metrics Server Requirement**

HPA requires metrics-server to function. Installation:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Verify with: `kubectl top nodes` and `kubectl top pods`

**Testing Autoscaling**

I used hey (HTTP load generator) to test:

```bash
hey -z 5m -c 200 -q 10 https://app.vasukapoor.com/api/
```

This simulates 200 concurrent users for 5 minutes. HPA responded:
- 0-30s: 3 pods (CPU usage climbing)
- 30-60s: Scaled to 6 pods (first scale up)
- 60-90s: Scaled to 10 pods (max replicas reached)
- After load: Maintained 10 pods for 5 minutes, then gradually scaled down

**Cluster Autoscaler Integration**

HPA scales pods. Cluster Autoscaler scales nodes.

When HPA requests more pods than fit on existing nodes, Cluster Autoscaler provisions additional nodes. They work together seamlessly.

**Custom Metrics with Prometheus**

For advanced use cases, HPA supports custom metrics:

- Request latency (scale up if p95 > 500ms)
- Queue depth (scale up if Celery queue > 100 tasks)
- Active connections (scale up if > 1000 connections per pod)

This requires Prometheus Adapter.

**Production Results**

After tuning HPA:
- Response time during spikes: <500ms (previously 2-3s)
- Cost savings: 40% reduction by scaling down during off-hours
- Availability: 99.9% uptime during traffic spikes
- Manual interventions: Zero (previously 3-5 per week)

**Common Pitfalls**

1. Forgetting resource requests - HPA fails silently
2. Setting scale-down stabilization too short - flapping
3. Not testing with realistic load - surprises in production
4. Ignoring cluster autoscaler - pods stay pending
5. Using default metrics only - missing application-specific signals

**Lessons Learned**

1. Always test autoscaling before production traffic hits
2. Monitor HPA events: `kubectl describe hpa`
3. Use metrics dashboards to tune thresholds
4. Document expected scaling behavior for oncall
5. Start conservative, then tune based on real traffic

HPA transformed my application from "hope it doesn't crash" to "bring on the traffic." The peace of mind is worth the tuning effort.''',
                'authors': 'Vasu Kapoor',
                'source': 'blog',
                'source_id': 'kubernetes-hpa-autoscaling',
                'url': None,
                'published_date': (datetime.now() - timedelta(days=12)).date(),
                'category': 'mlops',
                'tags': ['Kubernetes', 'Autoscaling', 'HPA', 'Performance', 'Cloud Native', 'DevOps'],
                'citation_count': 0,
                'relevance_score': 0.88,
                'is_featured': False
            },
            {
                'title': 'High Availability and Disaster Recovery for Cloud-Native Applications',
                'abstract': '''Building a resilient application isn't just about preventing failures - it's about recovering gracefully when they happen. I designed an HA/DR architecture for my portfolio backend achieving 99.9% availability and 5-minute recovery times.

**Understanding SLAs**

Service Level Agreements define reliability targets:
- 99.9% availability = 43 minutes downtime/month
- 99.95% availability = 22 minutes downtime/month
- 99.99% availability = 4 minutes downtime/month

Each additional "9" significantly increases complexity and cost.

**Multi-Region Architecture**

I deployed across two GCP regions (us-central1 primary, us-east1 failover):

Primary Region:
- Cloud Run (auto-scaling web servers)
- Cloud SQL PostgreSQL (read replicas enabled)
- Cloud Storage (default location)

Secondary Region:
- Cloud Run (warm standby, minimal instances)
- Cloud SQL (read replica promoted to master on failover)
- Cloud Storage (geo-redundant replication)

**Database Replication Strategy**

Cloud SQL provides async replication:
- Primary database writes to secondary with <1 second lag
- Read replicas serve read-only queries (reduces primary load)
- Automatic failover option (promoted in ~60 seconds)

**Global Load Balancing**

Google Cloud Load Balancer distributes traffic:
- Health checks every 10 seconds
- Removes unhealthy backends automatically
- Routes traffic to nearest healthy region
- SSL termination at load balancer

**Health Check Design**

Critical endpoint `/health/` checks:
- Database connectivity (query execution)
- Redis connectivity (ping/pong)
- Storage access (test write/read/delete)
- API response time (<2 seconds passes)

If any check fails, load balancer removes the instance.

**Backup Strategy**

3-2-1 backup rule:
- 3 copies of data
- 2 different storage types (disk + object storage)
- 1 copy offsite (different region)

Database backups:
- Automated daily backups (retained 30 days)
- Transaction logs (point-in-time recovery to any second)
- Weekly manual snapshots (retained 1 year)

Application state:
- Session data in Redis (replicated)
- Media files in Cloud Storage (geo-redundant)
- Configuration in Git (version controlled)

**Disaster Recovery Scenarios**

Scenario 1: Pod Crash
- Detection: <10 seconds (liveness probe)
- Recovery: Automatic restart
- Impact: Zero (other pods handle traffic)

Scenario 2: Region Outage
- Detection: 30 seconds (health checks fail)
- Recovery: Traffic routed to secondary region
- Impact: ~1 minute of increased latency

Scenario 3: Data Corruption
- Detection: Monitoring alerts
- Recovery: Restore from backup + replay transaction logs
- Impact: 15 minutes downtime

**RTO and RPO Targets**

Recovery Time Objective (RTO): How fast can we recover?
- Target: 15 minutes for complete recovery
- Achieved: 12 minutes average

Recovery Point Objective (RPO): How much data can we lose?
- Target: 5 minutes of data
- Achieved: <1 minute (transaction log frequency)

**Monitoring and Alerting**

Cloud Operations (formerly Stackdriver) monitors:
- Uptime checks (ping endpoints every minute from 6 global locations)
- Error rates (alert if >1% of requests fail)
- Latency (alert if p95 > 500ms for 5 minutes)
- Resource utilization (alert if CPU > 80%)

Alerts go to PagerDuty → on-call engineer.

**Failover Testing**

Monthly DR drills simulate:
- Region outage (disable all instances in primary)
- Database failure (kill primary database)
- Storage unavailability (block access to Cloud Storage)

Each test validates:
- Automatic failover works
- Monitoring detects failure
- Team receives alerts
- Recovery completes within RTO

**Cost Analysis**

HA/DR doesn't have to break the bank:
- Multi-region deployment: +30% cost
- Database replicas: +20% cost
- Geo-redundant storage: +15% cost
- Monitoring and logging: +10% cost

Total increase: ~75% for 99.9% availability vs single-region 95% availability.

For my portfolio: $68/month single-region → $106/month HA/DR.

**Lessons Learned**

1. Test failover regularly - assumptions are dangerous
2. Automate recovery - manual intervention is too slow
3. Monitor everything - you can't fix what you can't see
4. Document runbooks - panic + memory = bad outcomes
5. Practice chaos engineering - break things on purpose

**Results**

Since implementing HA/DR:
- Uptime: 99.92% (target: 99.9%)
- Incident response time: <5 minutes
- Data loss events: Zero
- Unplanned downtime: 28 minutes in 6 months

The peace of mind knowing the system can withstand failures is invaluable.''',
                'authors': 'Vasu Kapoor',
                'source': 'blog',
                'source_id': 'ha-dr-cloud-native',
                'url': None,
                'published_date': (datetime.now() - timedelta(days=3)).date(),
                'category': 'mlops',
                'tags': ['HA/DR', 'Reliability', 'SRE', 'Cloud', 'GCP', 'Architecture', 'DevOps'],
                'citation_count': 0,
                'relevance_score': 0.87,
                'is_featured': True
            },
            {
                'title': 'Optimizing Docker Images: From 1.2GB to 480MB with Multi-Stage Builds',
                'abstract': '''Large Docker images slow down deployments, increase storage costs, and expand attack surface. I reduced my Django application image from 1.2GB to 480MB using multi-stage builds and smart optimization techniques.

**The Baseline: Single-Stage Build**

My original Dockerfile:

```dockerfile
FROM python:3.11
COPY . /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "config.wsgi"]
```

Size: 1.2GB
Build time: 4 minutes
Deployment time: 2 minutes

**Problem Analysis**

Large size came from:
- Build tools (gcc, make, python-dev) not needed at runtime
- pip cache and wheel files
- Unused Python packages
- Source files (.git, .pyc, __pycache__)

**Multi-Stage Build Solution**

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends gcc
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
COPY . /app
CMD ["gunicorn", "config.wsgi"]
```

Size: 680MB (43% reduction)

**Further Optimization: Alpine Linux**

Switching to Alpine:

```dockerfile
FROM python:3.11-alpine AS builder
RUN apk add --no-cache gcc musl-dev postgresql-dev
# ... rest of build

FROM python:3.11-alpine
# ... runtime
```

Size: 480MB (60% total reduction)

**Layer Caching Strategy**

Docker caches layers. Order matters:

1. Base image (changes rarely)
2. System packages (changes occasionally)
3. Python dependencies (changes occasionally)
4. Application code (changes frequently)

This minimizes rebuild time when only code changes.

**Security Benefits**

Smaller images have:
- Fewer dependencies = smaller attack surface
- Fewer CVEs to patch
- Faster security scanning
- Smaller blast radius if compromised

**The .dockerignore File**

Critical for size reduction:

```
.git
__pycache__
*.pyc
.env
venv/
.vscode/
*.md
tests/
```

This prevented 200MB of unnecessary files from being copied.

**Non-Root User**

Running as root is a security risk:

```dockerfile
RUN addgroup --system app && adduser --system --group app
USER app
```

If the container is compromised, attacker has limited privileges.

**Build Time Optimization**

BuildKit parallel builds:

```bash
DOCKER_BUILDKIT=1 docker build .
```

BuildKit builds independent stages in parallel, reducing build time from 4 minutes to 90 seconds.

**Production Results**

After optimization:
- Image size: 480MB (60% reduction)
- Build time: 90 seconds (62% faster)
- Push time: 25 seconds (was 120 seconds)
- Deployment time: 45 seconds (was 2 minutes)
- Registry storage costs: 60% reduction

**Lessons Learned**

1. Always use multi-stage builds for compiled languages
2. Choose base images carefully (slim > full, alpine > slim)
3. Use .dockerignore religiously
4. Run as non-root user
5. Enable BuildKit for faster builds
6. Monitor image sizes in CI/CD

For Python specifically:
- Use --no-cache-dir with pip
- Remove *.pyc files
- Don't install dev dependencies in production

**Trade-offs**

Alpine advantages:
- Smallest size
- Minimal attack surface

Alpine disadvantages:
- musl libc vs glibc (compatibility issues with some packages)
- Longer build times (compile more from source)
- Less community support

For maximum compatibility, use python:3.11-slim instead of alpine.

The 60% size reduction dramatically improved deployment speed and reduced costs. Well worth the 2 hours of optimization effort.''',
                'authors': 'Vasu Kapoor',
                'source': 'blog',
                'source_id': 'docker-multi-stage-optimization',
                'url': None,
                'published_date': (datetime.now() - timedelta(days=15)).date(),
                'category': 'mlops',
                'tags': ['Docker', 'Containers', 'Optimization', 'DevOps', 'Security', 'Python'],
                'citation_count': 0,
                'relevance_score': 0.85,
                'is_featured': False
            },
        ]

        created_count = 0
        for post_data in blog_posts:
            try:
                post = Paper.objects.create(**post_data)
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {post.title[:60]}...'))
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to create post: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Successfully created {created_count} blog posts!'))
        self.stdout.write(self.style.SUCCESS(f'Total posts in database: {Paper.objects.count()}'))
