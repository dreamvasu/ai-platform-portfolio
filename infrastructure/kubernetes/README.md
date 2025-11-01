# Kubernetes Deployment for AI/ML Portfolio

This directory contains Kubernetes manifests for deploying the portfolio backend to a Kubernetes cluster.

## Architecture

```
Internet
    ↓
LoadBalancer Service (port 80)
    ↓
Django Pods (port 8000) [2-10 replicas]
    ↓
Vertex AI APIs (Embeddings + Gemini)
    ↓
ChromaDB (in-pod persistent storage)
```

## Prerequisites

1. **Kubernetes Cluster** (Minikube, GKE, EKS, or AKS)
2. **kubectl** CLI installed and configured
3. **Docker image** pushed to container registry
4. **GCP Service Account Key** for Vertex AI access

## Setup

### 1. Create GCP Credentials Secret

```bash
# Create secret from service account key file
kubectl create secret generic gcp-credentials \
  --from-file=key.json=/path/to/your-service-account-key.json \
  --from-literal=project_id=your-gcp-project-id
```

### 2. Build and Push Docker Image

```bash
# Build image
cd backend
docker build -t gcr.io/YOUR_PROJECT_ID/portfolio-backend:latest .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/portfolio-backend:latest
```

### 3. Update deployment.yaml

Replace `PROJECT_ID` in `deployment.yaml` with your actual GCP project ID:

```yaml
image: gcr.io/YOUR_PROJECT_ID/portfolio-backend:latest
```

### 4. Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml

# Verify deployment
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get hpa
```

## Monitoring

### View Pod Status
```bash
kubectl get pods -l app=portfolio -w
```

### View Logs
```bash
# Get pod name
kubectl get pods -l app=portfolio

# Stream logs
kubectl logs -f POD_NAME

# View logs from all pods
kubectl logs -l app=portfolio --tail=100
```

### Check HPA Status
```bash
kubectl get hpa portfolio-backend-hpa -w
```

### Describe Resources
```bash
kubectl describe deployment portfolio-backend
kubectl describe service portfolio-backend-service
kubectl describe hpa portfolio-backend-hpa
```

## Scaling

### Manual Scaling
```bash
# Scale to 5 replicas
kubectl scale deployment portfolio-backend --replicas=5

# Verify
kubectl get pods -l app=portfolio
```

### Auto-Scaling
The HPA automatically scales between 2-10 replicas based on:
- CPU utilization target: 70%
- Memory utilization target: 80%

## Access the Application

### Get Load Balancer IP
```bash
kubectl get service portfolio-backend-service

# Wait for EXTERNAL-IP (may take a few minutes)
# Then access at http://EXTERNAL-IP/
```

### Port Forward (for local testing)
```bash
kubectl port-forward service/portfolio-backend-service 8000:80

# Access at http://localhost:8000/
```

## Troubleshooting

### Pod Not Starting
```bash
# Check pod events
kubectl describe pod POD_NAME

# Common issues:
# - Image pull errors (check image name/tag)
# - Missing secrets (check gcp-credentials secret exists)
# - Resource limits (check node capacity)
```

### Pod Crashing
```bash
# View logs
kubectl logs POD_NAME

# Check previous container logs
kubectl logs POD_NAME --previous

# Common issues:
# - Missing GCP credentials
# - Vertex AI API not enabled
# - Database connection errors
```

### Service Not Accessible
```bash
# Check service endpoints
kubectl get endpoints portfolio-backend-service

# Check if pods are ready
kubectl get pods -l app=portfolio

# Verify network policies
kubectl get networkpolicies
```

## Configuration

### Resource Limits

Current configuration per pod:
- **Requests:** 512Mi memory, 250m CPU
- **Limits:** 1Gi memory, 500m CPU

Adjust in `deployment.yaml` based on workload:

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"
```

### Health Checks

**Liveness Probe:** Restarts pod if health check fails
- Path: `/api/chatbot/health/`
- Initial delay: 30s
- Period: 10s

**Readiness Probe:** Removes pod from service if not ready
- Path: `/api/chatbot/health/`
- Initial delay: 5s
- Period: 5s

## Clean Up

```bash
# Delete all resources
kubectl delete -f hpa.yaml
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
kubectl delete secret gcp-credentials

# Or delete by labels
kubectl delete all -l app=portfolio
```

## Production Considerations

1. **Persistent Storage:** Add PersistentVolumeClaim for ChromaDB
2. **Ingress:** Add Ingress controller for HTTPS and domain routing
3. **Monitoring:** Integrate Prometheus/Grafana for metrics
4. **Logging:** Ship logs to centralized logging (ELK, Cloud Logging)
5. **Secrets Management:** Use Sealed Secrets or external secrets operator
6. **Network Policies:** Restrict pod-to-pod communication
7. **Pod Disruption Budget:** Ensure availability during updates
8. **Resource Quotas:** Set namespace-level resource limits
9. **Rolling Updates:** Configure update strategy for zero-downtime deployments
10. **Backup:** Regular backups of ChromaDB data

## Cost Optimization

For GKE specifically:
- Use **GKE Autopilot** for serverless Kubernetes (no node management)
- Enable **Cluster Autoscaler** to scale nodes with workload
- Use **Spot/Preemptible VMs** for non-critical workloads (60-90% cost savings)
- Set **Pod Disruption Budgets** to allow node terminations
- Use **Workload Identity** instead of service account keys (more secure)

## Next Steps

1. Implement persistent storage for ChromaDB
2. Add Ingress with TLS termination
3. Set up monitoring and alerting
4. Configure CI/CD pipeline for automated deployments
5. Add horizontal pod autoscaling based on custom metrics (e.g., request queue length)
