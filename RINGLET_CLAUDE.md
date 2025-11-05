# Ringlet - Learning Management System

**Django-based LMS deployed to Azure Kubernetes Service with Terraform IaC**

---

## 🎯 Project Overview

**What is Ringlet?**
Ringlet is a production-grade Learning Management System (LMS) built with Django. It provides course management, user enrollment, assessments, and content delivery.

**Current Deployment Target:**
Azure Kubernetes Service (AKS) with production-ready infrastructure provisioned via Terraform.

**Tech Stack:**
- **Backend:** Django 4.2+, Django REST Framework
- **Database:** PostgreSQL (StatefulSet in Kubernetes)
- **Cache:** Redis
- **Task Queue:** Celery + Celery Beat
- **Web Server:** Gunicorn
- **Orchestration:** Kubernetes (AKS)
- **Infrastructure:** Terraform
- **Container:** Docker (multi-stage build)

---

## 📁 Project Structure

```
ringlet/
├── manage.py                    # Django management
├── config/                      # Django project config (or ringlet/)
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── wsgi.py
│   ├── urls.py
│   └── celery.py
├── apps/                        # Django applications
│   ├── courses/
│   ├── users/
│   ├── assessments/
│   └── ...
├── static/                      # Static files
├── media/                       # User uploads
├── requirements.txt             # Python dependencies
│
├── Dockerfile                   # Multi-stage production build
├── .dockerignore               # Build optimization
│
├── terraform/                   # Infrastructure as Code
│   ├── modules/
│   │   ├── networking/         # VNet, subnets, NSGs
│   │   ├── aks-cluster/        # AKS cluster config
│   │   ├── acr/                # Azure Container Registry
│   │   └── storage/            # Azure Files storage
│   └── environments/
│       ├── dev/                # Dev environment
│       └── prod/               # Production environment
│
├── kubernetes/                  # Kubernetes manifests
│   ├── base/
│   │   ├── postgres-statefulset.yaml
│   │   ├── redis-deployment.yaml
│   │   ├── django-deployment.yaml
│   │   ├── celery-worker-deployment.yaml
│   │   ├── celery-beat-deployment.yaml
│   │   ├── configmap.yaml
│   │   └── ingress.yaml
│   └── README.md
│
├── RINGLET_DEPLOYMENT_GUIDE.md  # Complete deployment guide
├── RINGLET_AKS_COMPLETION_STATUS.md
└── CLAUDE.md                    # This file
```

---

## 🏗️ Architecture

### Production Architecture on AKS

```
┌─────────────────────────────────────────────────────────────┐
│                      Azure Cloud                            │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              AKS Cluster (ringlet-prod-aks)        │    │
│  │                                                      │    │
│  │  ┌─────────────────────────────────────────────┐   │    │
│  │  │  Namespace: ringlet                         │   │    │
│  │  │                                              │   │    │
│  │  │  ┌──────────────┐  ┌──────────────┐        │   │    │
│  │  │  │   Django     │  │   Django     │  ...   │   │    │
│  │  │  │   (Pod 1)    │  │   (Pod 2)    │  (3-10)│   │    │
│  │  │  └──────────────┘  └──────────────┘        │   │    │
│  │  │         ▲                ▲                  │   │    │
│  │  │         │  Horizontal Pod Autoscaler (HPA) │   │    │
│  │  │         │                                   │   │    │
│  │  │  ┌──────────────┐  ┌──────────────┐        │   │    │
│  │  │  │Celery Worker │  │Celery Worker │  ...   │   │    │
│  │  │  │   (Pod 1)    │  │   (Pod 2)    │  (2-6) │   │    │
│  │  │  └──────────────┘  └──────────────┘        │   │    │
│  │  │         ▲                ▲                  │   │    │
│  │  │         │  Horizontal Pod Autoscaler (HPA) │   │    │
│  │  │         │                                   │   │    │
│  │  │  ┌──────────────┐                          │   │    │
│  │  │  │Celery Beat   │  (Singleton)             │   │    │
│  │  │  │  (1 Pod)     │                          │   │    │
│  │  │  └──────────────┘                          │   │    │
│  │  │         │                                   │   │    │
│  │  │         ▼                                   │   │    │
│  │  │  ┌──────────────┐  ┌──────────────┐        │   │    │
│  │  │  │  PostgreSQL  │  │    Redis     │        │   │    │
│  │  │  │(StatefulSet) │  │ (Deployment) │        │   │    │
│  │  │  └──────────────┘  └──────────────┘        │   │    │
│  │  │         │                 │                 │   │    │
│  │  │         ▼                 ▼                 │   │    │
│  │  │  ┌──────────────┐  ┌──────────────┐        │   │    │
│  │  │  │ Managed Disk │  │ Managed Disk │        │   │    │
│  │  │  │    (20GB)    │  │    (5GB)     │        │   │    │
│  │  │  └──────────────┘  └──────────────┘        │   │    │
│  │  │                                              │   │    │
│  │  │  Shared Storage (Azure Files):              │   │    │
│  │  │  ┌──────────────┐  ┌──────────────┐        │   │    │
│  │  │  │  Media Files │  │ Static Files │        │   │    │
│  │  │  │    (50GB)    │  │    (10GB)    │        │   │    │
│  │  │  └──────────────┘  └──────────────┘        │   │    │
│  │  │                                              │   │    │
│  │  └─────────────────────────────────────────────┘   │    │
│  │                                                      │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────┐  ┌──────────────────────┐          │
│  │  Container Registry│  │  Storage Account     │          │
│  │  (ringletprodacr)  │  │  (Azure Files)       │          │
│  └────────────────────┘  └──────────────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Component Details

**Django Pods (3-10 replicas):**
- Gunicorn WSGI server (4 workers per pod)
- Health checks on `/health/` endpoint
- Autoscaling based on CPU (70%) and Memory (75%)
- Init containers: wait-for-db, wait-for-redis, migrate, collectstatic

**Celery Workers (2-6 replicas):**
- 4 concurrent workers per pod
- Max 100 tasks per child (prevent memory leaks)
- Autoscaling based on CPU and Memory

**Celery Beat (1 replica):**
- Singleton scheduler (critical!)
- Database-backed scheduler (django-celery-beat)
- Recreate strategy (no rolling updates)

**PostgreSQL (StatefulSet):**
- 1 replica (can scale for HA)
- 20GB Azure Managed Disk (ReadWriteOnce)
- Persistent data across pod restarts

**Redis (Deployment):**
- 1 replica with AOF persistence
- 5GB Azure Managed Disk

**Shared Storage (Azure Files):**
- Media files: 50GB (ReadWriteMany)
- Static files: 10GB (ReadWriteMany)
- Accessible by all Django pods

---

## 🚀 Deployment Instructions

### Prerequisites

1. **Azure Account** with active subscription
2. **Tools Installed:**
   ```bash
   az --version       # Azure CLI
   terraform --version # Terraform 1.5+
   kubectl version    # kubectl
   docker --version   # Docker
   ```
3. **Logged in to Azure:**
   ```bash
   az login
   az account set --subscription "YOUR_SUBSCRIPTION"
   ```

### Quick Deploy

**IMPORTANT:** Follow the complete guide in `RINGLET_DEPLOYMENT_GUIDE.md`

**Summary:**

1. **Provision Infrastructure (3-4 hours)**
   ```bash
   cd terraform/environments/prod
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   terraform init
   terraform plan -out=tfplan
   terraform apply tfplan
   ```

2. **Build and Push Docker Image (1 hour)**
   ```bash
   az acr login --name ringletprodacr
   docker build -t ringletprodacr.azurecr.io/ringlet:latest .
   docker push ringletprodacr.azurecr.io/ringlet:latest
   ```

3. **Deploy to Kubernetes (2-3 hours)**
   ```bash
   az aks get-credentials --resource-group ringlet-prod-rg --name ringlet-prod-aks
   kubectl apply -f kubernetes/base/
   kubectl get pods -n ringlet -w
   ```

4. **Test Application**
   ```bash
   kubectl port-forward svc/django 8000:8000 -n ringlet
   curl http://localhost:8000/health/
   ```

---

## 🛠️ Common Tasks

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run Celery worker (in another terminal)
celery -A config worker --loglevel=info

# Run Celery beat (in another terminal)
celery -A config beat --loglevel=info
```

### Update Deployment

```bash
# Build new image
docker build -t ringletprodacr.azurecr.io/ringlet:v1.1.0 .

# Push to ACR
docker push ringletprodacr.azurecr.io/ringlet:v1.1.0

# Update Kubernetes deployment
kubectl set image deployment/django \
  django=ringletprodacr.azurecr.io/ringlet:v1.1.0 \
  -n ringlet

# Watch rollout
kubectl rollout status deployment/django -n ringlet
```

### Run Migrations in Kubernetes

```bash
# Get Django pod name
POD=$(kubectl get pod -n ringlet -l app=django -o jsonpath='{.items[0].metadata.name}')

# Run migrations
kubectl exec -it $POD -n ringlet -- python manage.py migrate

# Create superuser
kubectl exec -it $POD -n ringlet -- python manage.py createsuperuser
```

### View Logs

```bash
# Django logs
kubectl logs -f deployment/django -n ringlet --tail=100

# Celery worker logs
kubectl logs -f deployment/celery-worker -n ringlet --tail=100

# PostgreSQL logs
kubectl logs -f statefulset/postgres -n ringlet --tail=100
```

### Scale Manually

```bash
# Scale Django pods
kubectl scale deployment/django --replicas=5 -n ringlet

# Scale Celery workers
kubectl scale deployment/celery-worker --replicas=4 -n ringlet

# View HPA status
kubectl get hpa -n ringlet
```

### Access Database

```bash
# Port forward to PostgreSQL
kubectl port-forward statefulset/postgres 5432:5432 -n ringlet

# Connect with psql (in another terminal)
psql -h localhost -U ringlet -d ringlet_prod
```

---

## 🔧 Important File Locations

### Django Settings

- **Base settings:** `config/settings/base.py` (or `ringlet/settings/base.py`)
- **Production settings:** `config/settings/production.py`
- **WSGI:** `config/wsgi.py`

### Celery Configuration

- **Celery config:** `config/celery.py`
- **Tasks:** Look in each app's `tasks.py` (e.g., `apps/courses/tasks.py`)

### Kubernetes Configuration

- **All manifests:** `kubernetes/base/`
- **ConfigMap (env vars):** `kubernetes/base/configmap.yaml`
- **Secrets:** Created via kubectl, not in files

### Terraform Configuration

- **Modules:** `terraform/modules/`
- **Production config:** `terraform/environments/prod/`
- **Variables:** `terraform/environments/prod/terraform.tfvars`

---

## 📝 Important Notes for Claude Code

### When helping with this project:

1. **Django Settings Module:**
   - Check if Ringlet uses `config.settings` or `ringlet.settings`
   - Verify the WSGI path in `wsgi.py`
   - Update Dockerfile CMD if needed

2. **Database Credentials:**
   - NEVER commit database passwords to git
   - Use Kubernetes secrets: `kubectl create secret generic database-secret`
   - Reference in `kubernetes/base/configmap.yaml`

3. **Celery Beat:**
   - ALWAYS use exactly 1 replica (singleton pattern)
   - Use Recreate strategy, NOT RollingUpdate
   - Database-backed scheduler required

4. **File Paths:**
   - Media files: `/app/media` (Azure Files, RWX)
   - Static files: `/app/staticfiles` (Azure Files, RWX)
   - PostgreSQL data: `/var/lib/postgresql/data` (Managed Disk, RWO)

5. **Health Check Endpoint:**
   - Create `/health/` endpoint in Django
   - Should check: database connection, Redis connection
   - Used by Kubernetes liveness/readiness probes

6. **Init Containers:**
   - Always wait for dependencies (PostgreSQL, Redis) before starting
   - Run migrations in init container (before main app starts)
   - Collect static files in init container

7. **Security:**
   - Container runs as non-root user (UID 1000)
   - Secrets managed via Kubernetes secrets
   - No sensitive data in ConfigMaps

---

## 🎯 Project Goals

**Why this deployment exists:**

1. **Learning Sprint:** Demonstrate Kubernetes + Terraform skills for job applications
2. **Production-Ready:** Show best practices, not toy projects
3. **Portfolio Piece:** Prove ability to deploy complex multi-component systems
4. **Interview Prep:** Have actual code to discuss in technical interviews

**Skills Demonstrated:**

- Infrastructure as Code (Terraform)
- Kubernetes orchestration
- Container management (Docker)
- Cloud platforms (Azure)
- Production deployments (HA, autoscaling, monitoring)
- Django best practices
- Distributed systems (web, workers, scheduler, databases)

---

## 📚 Reference Documentation

1. **RINGLET_DEPLOYMENT_GUIDE.md** - Complete step-by-step deployment guide
2. **RINGLET_AKS_COMPLETION_STATUS.md** - What was built, interview prep
3. **terraform/README.md** - Terraform module documentation
4. **kubernetes/README.md** - Kubernetes deployment details

---

## 🐛 Troubleshooting

### Common Issues

**Pods not starting:**
```bash
kubectl describe pod <pod-name> -n ringlet
kubectl logs <pod-name> -n ringlet
```

**Database connection errors:**
- Check PostgreSQL pod is running
- Verify database secret exists
- Check ConfigMap has correct DB_HOST (should be `postgres`)

**Init container failures:**
- Usually means PostgreSQL/Redis not ready yet
- Check their pod status first

**Image pull errors:**
- Verify ACR integration: `az aks check-acr`
- Check image exists in ACR
- Verify AKS has AcrPull role

---

## ✅ Health Check Endpoint

Create this in Django if it doesn't exist:

```python
# config/urls.py or ringlet/urls.py
from django.http import JsonResponse
from django.db import connection
from django_redis import get_redis_connection

def health_check(request):
    try:
        # Check database
        connection.ensure_connection()

        # Check Redis
        redis_conn = get_redis_connection("default")
        redis_conn.ping()

        return JsonResponse({"status": "healthy"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "unhealthy", "error": str(e)}, status=503)

urlpatterns = [
    path('health/', health_check),
    # ... other patterns
]
```

---

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] Django SECRET_KEY generated and in Kubernetes secret
- [ ] Database password strong and in Kubernetes secret
- [ ] ALLOWED_HOSTS set correctly in ConfigMap
- [ ] DEBUG=False in production settings
- [ ] Static files collected (init container does this)
- [ ] Migrations run (init container does this)
- [ ] Superuser created (do manually after first deploy)
- [ ] Health check endpoint working
- [ ] Celery tasks registered
- [ ] Environment variables reviewed
- [ ] Resource limits set on all pods
- [ ] HPA configured correctly
- [ ] Backup strategy planned

---

## 💰 Cost Estimate

**Production (Full Scale):** ~$400-1,100/month
**Development (Minimal):** ~$100-200/month

**Cost Optimization:**
- Stop cluster when not in use: `az aks stop`
- Use smaller VM sizes for dev
- Delete resources: `terraform destroy` (CAREFUL!)

---

**Last Updated:** November 2, 2025
**Deployment Target:** Azure Kubernetes Service (AKS)
**Infrastructure:** Terraform
**Status:** Ready to deploy ✅
