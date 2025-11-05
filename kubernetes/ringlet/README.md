# ☸️ Ringlet Kubernetes Deployment

**Production-ready Kubernetes manifests for Ringlet Django LMS on Azure AKS**

---

## 📁 Structure

```
kubernetes/ringlet/
├── base/                           # Base Kubernetes manifests
│   ├── postgres-statefulset.yaml  # PostgreSQL with persistent storage
│   ├── redis-deployment.yaml      # Redis cache
│   ├── django-deployment.yaml     # Django web application
│   ├── django-hpa.yaml            # Horizontal Pod Autoscaler (3-10 pods)
│   ├── celery-worker-deployment.yaml  # Celery async workers (2-6 pods)
│   ├── celery-beat-deployment.yaml    # Celery scheduler (1 pod)
│   ├── configmap.yaml             # Application configuration
│   └── ingress.yaml               # NGINX Ingress Controller
│
├── overlays/                      # Kustomize overlays (optional)
│   ├── dev/
│   └── prod/
│
├── Dockerfile                     # Multi-stage production image
├── .dockerignore
├── requirements.txt
└── README.md
```

---

## 🎯 Architecture

### Components

**1. PostgreSQL StatefulSet**
- 1 replica (can scale for HA)
- Persistent volume (20GB Azure Managed Disk)
- Health checks and probes
- Dedicated headless service

**2. Redis Deployment**
- 1 replica with persistence
- 5GB persistent volume
- AOF (Append-Only File) enabled

**3. Django Deployment**
- 3-10 replicas (autoscaling)
- Init containers for migrations and collectstatic
- Health checks on /health/ endpoint
- Shared media/static storage (Azure Files)

**4. Celery Workers**
- 2-6 replicas (autoscaling)
- Concurrent task processing (4 workers per pod)
- Max 100 tasks per child
- HPA based on CPU/memory

**5. Celery Beat**
- 1 replica (singleton scheduler)
- Database-backed scheduler
- Recreate strategy (no rolling updates)

---

## 🚀 Quick Deploy

### Prerequisites

```bash
# 1. AKS cluster running
kubectl get nodes

# 2. ACR with Docker image
az acr repository list --name ringletprodacr

# 3. Namespace created
kubectl create namespace ringlet
```

### Deploy All Components

```bash
cd kubernetes/ringlet/base

# Apply in order
kubectl apply -f postgres-statefulset.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f configmap.yaml

# Wait for databases
kubectl wait --for=condition=ready pod -l app=postgres -n ringlet --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n ringlet --timeout=120s

# Deploy application
kubectl apply -f django-deployment.yaml
kubectl apply -f django-hpa.yaml
kubectl apply -f celery-worker-deployment.yaml
kubectl apply -f celery-beat-deployment.yaml

# Optional: Ingress
kubectl apply -f ingress.yaml
```

### Verify Deployment

```bash
# Check all resources
kubectl get all -n ringlet

# Watch pods
kubectl get pods -n ringlet -w

# Check logs
kubectl logs -f deployment/django -n ringlet
kubectl logs -f deployment/celery-worker -n ringlet
```

---

## 🐳 Docker Image

### Build and Push

```bash
# Ensure you have Ringlet Django app code
cd /path/to/ringlet-app

# Copy build files
cp /path/to/kubernetes/ringlet/Dockerfile .
cp /path/to/kubernetes/ringlet/requirements.txt .
cp /path/to/kubernetes/ringlet/.dockerignore .

# Build
docker build -t ringletprodacr.azurecr.io/ringlet:v1.0.0 .
docker build -t ringletprodacr.azurecr.io/ringlet:latest .

# Login to ACR
az acr login --name ringletprodacr

# Push
docker push ringletprodacr.azurecr.io/ringlet:v1.0.0
docker push ringletprodacr.azurecr.io/ringlet:latest
```

### Multi-stage Build Benefits

- **Builder stage:** Install dependencies
- **Runtime stage:** Minimal production image
- Non-root user for security
- Health checks included
- Optimized for Gunicorn

**Final image size:** ~150-200MB (vs 1GB+ without optimization)

---

## ⚙️ Configuration

### Secrets (Required)

```bash
# Database credentials
kubectl create secret generic database-secret \
  --from-literal=POSTGRES_USER=ringlet \
  --from-literal=POSTGRES_PASSWORD='your-secure-password' \
  --from-literal=POSTGRES_DB=ringlet_prod \
  --namespace=ringlet

# Django secrets
kubectl create secret generic django-secret \
  --from-literal=SECRET_KEY="$(openssl rand -base64 50)" \
  --from-literal=EMAIL_HOST_USER="your-email@example.com" \
  --from-literal=EMAIL_HOST_PASSWORD="your-email-password" \
  --namespace=ringlet

# Azure Files (created by Terraform)
kubectl get secret azure-file-secret -n ringlet
```

### ConfigMap

Edit `configmap.yaml` to customize:

```yaml
ALLOWED_HOSTS: "ringlet.example.com"  # Your domain
DEBUG: "False"
TIME_ZONE: "America/New_York"
```

---

## 📈 Autoscaling

### Django HPA

**Current configuration:**
- Min replicas: 3
- Max replicas: 10
- Target CPU: 70%
- Target Memory: 75%
- Scale up: Fast (2x every 30s)
- Scale down: Slow (50% every 60s after 5min)

### Celery Worker HPA

**Current configuration:**
- Min replicas: 2
- Max replicas: 6
- Target CPU: 70%
- Target Memory: 75%

### Test Autoscaling

```bash
# Generate load
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c \
  "while sleep 0.01; do wget -q -O- http://django.ringlet:8000/; done"

# Watch HPA scale up
kubectl get hpa -n ringlet -w

# Stop load (Ctrl+C)
# Watch HPA scale down (takes ~5 minutes)
```

---

## 💾 Storage

### Persistent Volumes

**PostgreSQL:** Azure Managed Disk (RWO)
- Storage class: `managed-csi`
- Size: 20GB
- Access mode: ReadWriteOnce
- Backup: Volume snapshots

**Redis:** Azure Managed Disk (RWO)
- Storage class: `managed-csi`
- Size: 5GB
- Access mode: ReadWriteOnce

**Media Files:** Azure Files (RWX)
- Storage class: `azurefile-csi`
- Size: 50GB
- Access mode: ReadWriteMany
- Shared across Django pods

**Static Files:** Azure Files (RWX)
- Storage class: `azurefile-csi`
- Size: 10GB
- Access mode: ReadWriteMany
- Shared across Django pods

### Storage Best Practices

✅ **DO:**
- Use Azure Managed Disk for databases (better performance)
- Use Azure Files for shared storage (media/static)
- Enable backup/snapshots
- Monitor disk usage

❌ **DON'T:**
- Use Azure Files for databases (poor performance)
- Delete PVCs without backups
- Ignore storage quota warnings

---

## 🔍 Monitoring

### View Logs

```bash
# Django logs
kubectl logs -f deployment/django -n ringlet --tail=100

# Celery worker logs
kubectl logs -f deployment/celery-worker -n ringlet --tail=100

# Celery beat logs
kubectl logs -f deployment/celery-beat -n ringlet --tail=100

# PostgreSQL logs
kubectl logs -f statefulset/postgres -n ringlet --tail=100

# All pods with label
kubectl logs -f -l tier=web -n ringlet
```

### Resource Usage

```bash
# Node resource usage
kubectl top nodes

# Pod resource usage
kubectl top pods -n ringlet

# Specific deployment
kubectl top pods -n ringlet -l app=django
```

### Events

```bash
# All events in namespace
kubectl get events -n ringlet --sort-by='.lastTimestamp'

# Pod events
kubectl describe pod <pod-name> -n ringlet

# Deployment events
kubectl describe deployment django -n ringlet
```

---

## 🔄 Updates and Rollbacks

### Update Image

```bash
# Update to new version
kubectl set image deployment/django \
  django=ringletprodacr.azurecr.io/ringlet:v1.1.0 \
  -n ringlet

# Watch rollout
kubectl rollout status deployment/django -n ringlet
```

### Rollback

```bash
# Check rollout history
kubectl rollout history deployment/django -n ringlet

# Rollback to previous version
kubectl rollout undo deployment/django -n ringlet

# Rollback to specific revision
kubectl rollout undo deployment/django --to-revision=2 -n ringlet
```

### Restart Deployment

```bash
# Restart all pods (zero downtime)
kubectl rollout restart deployment/django -n ringlet
kubectl rollout restart deployment/celery-worker -n ringlet
```

---

## 🐛 Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n ringlet

# Describe pod for events
kubectl describe pod <pod-name> -n ringlet

# Check logs
kubectl logs <pod-name> -n ringlet

# Check previous logs (if crashlooping)
kubectl logs <pod-name> -n ringlet --previous
```

### Common Issues

**1. ImagePullBackOff**
```bash
# Check ACR integration
kubectl describe pod <pod-name> -n ringlet | grep -A 5 Events

# Verify image exists
az acr repository show-tags --name ringletprodacr --repository ringlet

# Check AKS-ACR role assignment
az aks check-acr --name ringlet-prod-aks --resource-group ringlet-prod-rg --acr ringletprodacr.azurecr.io
```

**2. Init Container Failures**
```bash
# Check init container logs
kubectl logs <pod-name> -n ringlet -c wait-for-db
kubectl logs <pod-name> -n ringlet -c migrate

# Verify database is ready
kubectl exec -it postgres-0 -n ringlet -- psql -U ringlet -d ringlet_prod -c '\l'
```

**3. Storage Issues**
```bash
# Check PVCs
kubectl get pvc -n ringlet
kubectl describe pvc media-pvc -n ringlet

# Check storage classes
kubectl get storageclass

# Verify Azure Files
az storage share list --account-name ringletprodstorage --output table
```

**4. Database Connection Errors**
```bash
# Test database from Django pod
POD=$(kubectl get pod -n ringlet -l app=django -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $POD -n ringlet -- python manage.py dbshell

# Check database service
kubectl get svc postgres -n ringlet
kubectl describe svc postgres -n ringlet
```

---

## 🔐 Security

### Implemented

✅ Non-root container user
✅ Read-only root filesystem (where possible)
✅ Resource limits on all containers
✅ Network policies ready (need to enable)
✅ Secrets for sensitive data
✅ Least privilege RBAC

### Recommended Additions

- [ ] Pod Security Standards (restricted)
- [ ] Network policies
- [ ] Image scanning (Azure Defender)
- [ ] Secret encryption at rest
- [ ] Azure Key Vault integration

---

## 📊 Resource Requests/Limits

### Django
```yaml
requests:  memory: 512Mi,  cpu: 250m
limits:    memory: 1Gi,    cpu: 500m
```

### Celery Worker
```yaml
requests:  memory: 512Mi,  cpu: 250m
limits:    memory: 1Gi,    cpu: 500m
```

### PostgreSQL
```yaml
requests:  memory: 512Mi,  cpu: 250m
limits:    memory: 1Gi,    cpu: 500m
```

### Redis
```yaml
requests:  memory: 256Mi,  cpu: 100m
limits:    memory: 512Mi,  cpu: 200m
```

---

## 🎯 Production Readiness

### Checklist

- [x] Multi-stage Dockerfile
- [x] Non-root user
- [x] Health checks configured
- [x] Resource limits set
- [x] Horizontal autoscaling
- [x] Persistent storage
- [x] Init containers for migrations
- [x] ConfigMaps for configuration
- [x] Secrets for sensitive data
- [x] Rolling update strategy
- [x] Pod disruption budgets (recommended)
- [x] Readiness/liveness probes

---

**Created:** November 2, 2025
**Author:** Vasu Kapoor
**Purpose:** Production-ready Kubernetes deployment for learning sprint
