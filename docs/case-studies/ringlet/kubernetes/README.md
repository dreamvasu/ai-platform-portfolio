# Ringlet Kubernetes Deployment

Complete Kubernetes manifests for deploying Ringlet educational platform.

## Quick Deploy

```bash
# Apply all manifests
kubectl apply -k .

# Or apply individually
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f django-deployment.yaml
kubectl apply -f celery-deployment.yaml
kubectl apply -f ingress.yaml
kubectl apply -f hpa.yaml
```

## Prerequisites

1. **Kubernetes Cluster** (GKE, EKS, AKS, or local)
2. **kubectl** configured
3. **Container Registry** with Ringlet image
4. **Domain name** for ingress
5. **Storage classes** configured

## Architecture

```
┌─────────────────┐
│   Ingress       │ ← HTTPS (443)
│  (Load Balancer)│
└────────┬────────┘
         │
    ┌────┴─────┐
    │  Service │
    └────┬─────┘
         │
    ┌────▼─────────────┐
    │ Django Pods (3+) │ ← Auto-scaling
    │  - Gunicorn      │
    │  - Health checks │
    └──────┬───────────┘
           │
    ┌──────┴───────┬──────────┐
    │              │          │
┌───▼────┐   ┌────▼────┐  ┌──▼────────┐
│ PostgreSQL│   │  Redis  │  │  Celery   │
│ (Primary) │   │ (Cache) │  │ Workers   │
└───────────┘   └─────────┘  └───────────┘
```

## Components

### 1. Namespace
- Isolates Ringlet resources

### 2. ConfigMap
- Non-sensitive configuration
- Database connection strings
- Application settings

### 3. Secrets
- Sensitive credentials
- API keys
- Database passwords

### 4. PostgreSQL
- Persistent storage (10Gi)
- Health checks
- Single replica (upgrade to StatefulSet for HA)

### 5. Redis
- Cache and Celery broker
- Persistence with appendonly mode
- Single replica

### 6. Django Application
- 3 replicas (scales to 10)
- Init containers for migrations
- Health checks (/health/ endpoint)
- Persistent media storage

### 7. Celery Workers
- Background task processing
- 2 replicas (scales to 6)
- Celery Beat for scheduled tasks

### 8. Ingress
- HTTPS termination
- Load balancing
- Managed certificates (GKE)

### 9. Horizontal Pod Autoscaler
- CPU-based scaling (70%)
- Memory-based scaling (80%)
- Min 3, Max 10 pods

## Environment-Specific Setup

### Update secrets.yaml
```bash
# Generate Django secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Update secrets.yaml with:
# - SECRET_KEY
# - DB_PASSWORD
# - API keys
```

### Update configmap.yaml
```bash
# Set your domain
ALLOWED_HOSTS: "ringlet.yourcompany.com"
```

### Update ingress.yaml
```bash
# Replace:
- host: ringlet.example.com
# With:
- host: ringlet.yourcompany.com
```

### Update image registry
```bash
# In all deployment files, replace:
image: gcr.io/YOUR_PROJECT_ID/ringlet:latest
# With:
image: gcr.io/your-actual-project/ringlet:v1.0.0
```

## Deployment Steps

### 1. Build and push image
```bash
cd /path/to/ringlet
docker build -t gcr.io/YOUR_PROJECT_ID/ringlet:v1.0.0 .
docker push gcr.io/YOUR_PROJECT_ID/ringlet:v1.0.0
```

### 2. Create namespace
```bash
kubectl apply -f namespace.yaml
```

### 3. Deploy database and cache
```bash
kubectl apply -f postgres-deployment.yaml
kubectl apply -f redis-deployment.yaml

# Wait for them to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n ringlet --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n ringlet --timeout=60s
```

### 4. Apply configs and secrets
```bash
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml
```

### 5. Deploy application
```bash
kubectl apply -f django-deployment.yaml
kubectl apply -f celery-deployment.yaml
```

### 6. Setup ingress
```bash
# Reserve static IP (GKE)
gcloud compute addresses create ringlet-ip --global

# Get the IP
gcloud compute addresses describe ringlet-ip --global --format="get(address)"

# Point your domain to this IP in DNS

# Apply ingress
kubectl apply -f ingress.yaml
```

### 7. Enable auto-scaling
```bash
kubectl apply -f hpa.yaml
```

## Verify Deployment

```bash
# Check all resources
kubectl get all -n ringlet

# Check pods
kubectl get pods -n ringlet

# Check services
kubectl get svc -n ringlet

# Check ingress
kubectl get ingress -n ringlet

# Check HPA status
kubectl get hpa -n ringlet

# View logs
kubectl logs -f deployment/ringlet-django -n ringlet
kubectl logs -f deployment/ringlet-celery-worker -n ringlet

# Check pod resource usage
kubectl top pods -n ringlet
```

## Troubleshooting

### Pods not starting
```bash
# Describe pod
kubectl describe pod <pod-name> -n ringlet

# Check events
kubectl get events -n ringlet --sort-by='.lastTimestamp'
```

### Database connection issues
```bash
# Test PostgreSQL connectivity
kubectl run -it --rm debug --image=postgres:15-alpine --restart=Never -n ringlet -- psql -h postgres-service -U ringlet_user -d ringlet_db

# Check Redis
kubectl run -it --rm debug --image=redis:7-alpine --restart=Never -n ringlet -- redis-cli -h redis-service ping
```

### Migration failures
```bash
# Run migrations manually
kubectl exec -it deployment/ringlet-django -n ringlet -- python manage.py migrate
```

### Check ingress status
```bash
kubectl describe ingress ringlet-ingress -n ringlet
kubectl get managedcertificate ringlet-cert -n ringlet
```

## Scaling

### Manual scaling
```bash
# Scale Django pods
kubectl scale deployment ringlet-django -n ringlet --replicas=5

# Scale Celery workers
kubectl scale deployment ringlet-celery-worker -n ringlet --replicas=4
```

### Auto-scaling
HPA automatically adjusts replicas based on CPU/memory metrics.

## Updates / Rolling Deployment

```bash
# Update image
kubectl set image deployment/ringlet-django django=gcr.io/YOUR_PROJECT_ID/ringlet:v1.1.0 -n ringlet

# Check rollout status
kubectl rollout status deployment/ringlet-django -n ringlet

# Rollback if needed
kubectl rollout undo deployment/ringlet-django -n ringlet
```

## Cleanup

```bash
# Delete all resources
kubectl delete -k .

# Or delete namespace (removes everything)
kubectl delete namespace ringlet
```

## Production Considerations

1. **High Availability**
   - PostgreSQL: Use CloudSQL or StatefulSet with replication
   - Redis: Use Redis Cluster or managed service (Memorystore)

2. **Monitoring**
   - Add Prometheus metrics
   - Setup Grafana dashboards
   - Configure alerts

3. **Logging**
   - Use Fluentd/Fluent Bit
   - Ship logs to Cloud Logging/ELK

4. **Security**
   - Use external secret manager (Vault, Google Secret Manager)
   - Network policies
   - Pod security policies
   - RBAC

5. **Backup**
   - Database backups
   - PVC snapshots
   - Disaster recovery plan

6. **CI/CD**
   - Automate deployments
   - GitOps with ArgoCD/Flux

## Cost Optimization

- Use preemptible nodes for non-critical workloads
- Right-size resource requests/limits
- Use cluster autoscaler
- Implement pod disruption budgets
