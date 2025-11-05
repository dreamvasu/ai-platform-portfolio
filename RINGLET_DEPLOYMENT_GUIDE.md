# 🚀 Ringlet AKS Deployment Guide

**Complete step-by-step guide to deploy Ringlet LMS to Azure Kubernetes Service using Terraform**

---

## 📋 Prerequisites

### Required Tools
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install Terraform
brew install terraform  # macOS
# OR
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip && sudo mv terraform /usr/local/bin/

# Install kubectl
az aks install-cli

# Verify installations
az --version
terraform --version
kubectl version --client
```

### Azure Account
- Active Azure subscription
- Contributor role or higher
- Azure CLI logged in: `az login`

---

## 🏗️ Phase 1: Infrastructure Provisioning (3-4 hours)

### Step 1: Prepare Terraform Backend

Create storage account for Terraform state:

```bash
# Set variables
RESOURCE_GROUP="terraform-state-rg"
LOCATION="eastus"
STORAGE_ACCOUNT="tfstateringlet"
CONTAINER_NAME="tfstate"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create storage account
az storage account create \
  --resource-group $RESOURCE_GROUP \
  --name $STORAGE_ACCOUNT \
  --sku Standard_LRS \
  --encryption-services blob

# Get storage account key
ACCOUNT_KEY=$(az storage account keys list \
  --resource-group $RESOURCE_GROUP \
  --account-name $STORAGE_ACCOUNT \
  --query '[0].value' -o tsv)

# Create blob container
az storage container create \
  --name $CONTAINER_NAME \
  --account-name $STORAGE_ACCOUNT \
  --account-key $ACCOUNT_KEY

echo "✅ Terraform backend created!"
```

### Step 2: Configure Terraform Variables

```bash
cd terraform/environments/prod

# Copy example variables
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars
nano terraform.tfvars
```

**Update with your values:**
```hcl
location    = "eastus"
owner       = "your-name"
cost_center = "learning-sprint"

# Generate strong password
postgres_password = "$(openssl rand -base64 32)"

# Optional: Add your Azure AD admin group
# aks_admin_group_object_ids = ["YOUR-GROUP-OBJECT-ID"]
```

### Step 3: Initialize and Apply Terraform

```bash
cd terraform/environments/prod

# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Plan deployment (review changes)
terraform plan -out=tfplan

# Apply infrastructure (takes 15-20 minutes)
terraform apply tfplan

# Save outputs
terraform output > outputs.txt
cat outputs.txt
```

**Expected outputs:**
```
resource_group_name = "ringlet-prod-rg"
aks_cluster_name = "ringlet-prod-aks"
acr_login_server = "ringletprodacr.azurecr.io"
kube_config_command = "az aks get-credentials..."
```

### Step 4: Configure kubectl

```bash
# Get AKS credentials
az aks get-credentials \
  --resource-group ringlet-prod-rg \
  --name ringlet-prod-aks \
  --overwrite-existing

# Verify cluster access
kubectl get nodes
kubectl get namespaces

# Should see:
# NAME                STATUS   ROLES   AGE     VERSION
# aks-system-xxxxx    Ready    agent   5m      v1.28.x
# aks-user-xxxxx      Ready    agent   5m      v1.28.x
```

---

## 🐳 Phase 2: Build and Push Docker Image (1 hour)

### Step 1: Prepare Application Code

⚠️ **Important:** You need the actual Ringlet Django application code.

```bash
# If you have the Ringlet repo
git clone https://github.com/your-org/ringlet.git
cd ringlet

# Copy Dockerfile and requirements
cp ../ai-platform-portfolio/kubernetes/ringlet/Dockerfile .
cp ../ai-platform-portfolio/kubernetes/ringlet/requirements.txt .
cp ../ai-platform-portfolio/kubernetes/ringlet/.dockerignore .
```

### Step 2: Build Docker Image

```bash
# Login to ACR
az acr login --name ringletprodacr

# Build image (multi-stage for optimization)
docker build -t ringletprodacr.azurecr.io/ringlet:v1.0.0 .
docker build -t ringletprodacr.azurecr.io/ringlet:latest .

# Push to ACR
docker push ringletprodacr.azurecr.io/ringlet:v1.0.0
docker push ringletprodacr.azurecr.io/ringlet:latest

# Verify
az acr repository list --name ringletprodacr --output table
az acr repository show-tags --name ringletprodacr --repository ringlet
```

---

## ☸️ Phase 3: Deploy to Kubernetes (2-3 hours)

### Step 1: Create Kubernetes Secrets

```bash
# Database credentials
kubectl create secret generic database-secret \
  --from-literal=POSTGRES_USER=ringlet \
  --from-literal=POSTGRES_PASSWORD='YOUR_SECURE_PASSWORD' \
  --from-literal=POSTGRES_DB=ringlet_prod \
  --namespace=ringlet

# Django secret key
kubectl create secret generic django-secret \
  --from-literal=SECRET_KEY="$(openssl rand -base64 50)" \
  --from-literal=EMAIL_HOST_USER="your-email@example.com" \
  --from-literal=EMAIL_HOST_PASSWORD="your-email-password" \
  --namespace=ringlet

# Verify secrets
kubectl get secrets -n ringlet
```

### Step 2: Deploy Application Components

```bash
cd kubernetes/ringlet/base

# Deploy in order:
# 1. PostgreSQL
kubectl apply -f postgres-statefulset.yaml

# Wait for PostgreSQL to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n ringlet --timeout=300s

# 2. Redis
kubectl apply -f redis-deployment.yaml

# Wait for Redis
kubectl wait --for=condition=ready pod -l app=redis -n ringlet --timeout=120s

# 3. ConfigMap
kubectl apply -f configmap.yaml

# 4. Django application
kubectl apply -f django-deployment.yaml

# 5. Horizontal Pod Autoscaler for Django
kubectl apply -f django-hpa.yaml

# 6. Celery workers
kubectl apply -f celery-worker-deployment.yaml

# 7. Celery Beat scheduler
kubectl apply -f celery-beat-deployment.yaml

# 8. Ingress (optional - requires NGINX Ingress Controller)
# kubectl apply -f ingress.yaml
```

### Step 3: Verify Deployment

```bash
# Check all resources
kubectl get all -n ringlet

# Check pods
kubectl get pods -n ringlet -w

# Check services
kubectl get svc -n ringlet

# Check HPA
kubectl get hpa -n ringlet

# View logs
kubectl logs -f deployment/django -n ringlet
kubectl logs -f deployment/celery-worker -n ringlet
kubectl logs -f deployment/celery-beat -n ringlet
```

### Step 4: Test Application

```bash
# Port forward to Django service
kubectl port-forward svc/django 8000:8000 -n ringlet

# In another terminal, test
curl http://localhost:8000/health/
curl http://localhost:8000/admin/

# Or access in browser
open http://localhost:8000
```

---

## 🌐 Phase 4: Expose Application (Optional)

### Option 1: Load Balancer (Quick)

```bash
# Change Django service to LoadBalancer
kubectl patch svc django -n ringlet -p '{"spec": {"type": "LoadBalancer"}}'

# Get external IP (takes 2-3 minutes)
kubectl get svc django -n ringlet -w

# Access application
EXTERNAL_IP=$(kubectl get svc django -n ringlet -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Application URL: http://$EXTERNAL_IP:8000"
```

### Option 2: Ingress Controller (Production)

```bash
# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# Wait for ingress controller
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Apply Ingress
kubectl apply -f kubernetes/ringlet/base/ingress.yaml

# Get Ingress IP
kubectl get ingress -n ringlet

# Update DNS to point to Ingress IP
# ringlet.example.com → INGRESS_IP
```

---

## 📊 Monitoring and Validation

### Check Cluster Status

```bash
# Node status
kubectl top nodes

# Pod resource usage
kubectl top pods -n ringlet

# HPA status
kubectl get hpa -n ringlet -w

# Logs
kubectl logs -f -l app=django -n ringlet --tail=100
```

### Run Migrations

```bash
# If init container didn't run migrations, do manually:
POD=$(kubectl get pod -n ringlet -l app=django -o jsonpath='{.items[0].metadata.name}')

kubectl exec -it $POD -n ringlet -- python manage.py migrate
kubectl exec -it $POD -n ringlet -- python manage.py createsuperuser
```

### Test Autoscaling

```bash
# Generate load
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c \
  "while sleep 0.01; do wget -q -O- http://django.ringlet:8000/; done"

# Watch HPA scale up
kubectl get hpa django-hpa -n ringlet -w
```

---

## 🎯 Success Checklist

- [ ] Infrastructure provisioned with Terraform
- [ ] AKS cluster running (2 node pools)
- [ ] ACR created and Docker image pushed
- [ ] Azure Files storage configured
- [ ] PostgreSQL StatefulSet running
- [ ] Redis deployment running
- [ ] Django deployment (3+ pods)
- [ ] Celery workers (2+ pods)
- [ ] Celery Beat (1 pod)
- [ ] HPA configured and working
- [ ] Application accessible (port-forward or LoadBalancer)
- [ ] Database migrations completed
- [ ] Admin user created
- [ ] Static/media files accessible

---

## 💰 Cost Estimate

### Monthly Costs (Production)
```
AKS Cluster:
  - Control Plane: FREE
  - System Pool (1-3 x D2s_v3): $70-210/month
  - User Pool (2-6 x D4s_v3): $280-840/month

Azure Container Registry (Standard): $20/month
Azure Files (60GB): $12/month
Managed Disk (25GB): $3/month
Load Balancer: $20/month

TOTAL: $405-1,105/month (depending on scale)
```

### Cost Optimization Tips
```bash
# Use dev environment for learning (smaller VMs)
aks_system_vm_size = "Standard_B2s"  # $30/month
aks_user_vm_size = "Standard_B2ms"   # $60/month

# Stop cluster when not in use
az aks stop --name ringlet-prod-aks --resource-group ringlet-prod-rg

# Start when needed
az aks start --name ringlet-prod-aks --resource-group ringlet-prod-rg
```

---

## 🧹 Cleanup

### Delete Application (Keep Infrastructure)

```bash
# Delete Kubernetes resources
kubectl delete namespace ringlet

# Keep AKS cluster and ACR for future use
```

### Delete Everything

```bash
# Destroy Terraform resources (CAREFUL!)
cd terraform/environments/prod
terraform destroy

# Delete Terraform state storage (if no longer needed)
az group delete --name terraform-state-rg --yes --no-wait
```

---

## 🐛 Troubleshooting

### Pods Not Starting

```bash
# Check pod events
kubectl describe pod <pod-name> -n ringlet

# Check logs
kubectl logs <pod-name> -n ringlet

# Common issues:
# - Image pull errors: Check ACR login
# - Init containers failing: Check PostgreSQL/Redis connectivity
# - Crashloops: Check environment variables and secrets
```

### Database Connection Issues

```bash
# Check PostgreSQL pod
kubectl exec -it postgres-0 -n ringlet -- psql -U ringlet -d ringlet_prod

# Check database secret
kubectl get secret database-secret -n ringlet -o yaml

# Restart Django pods
kubectl rollout restart deployment/django -n ringlet
```

### Storage Issues

```bash
# Check PVCs
kubectl get pvc -n ringlet

# Check Azure Files
az storage share list --account-name ringletprodstorage

# Describe PVC for events
kubectl describe pvc media-pvc -n ringlet
```

---

## 📚 Next Steps

1. **Set up monitoring:** Azure Monitor, Prometheus, Grafana
2. **Configure CI/CD:** GitHub Actions, Azure DevOps
3. **Add TLS certificates:** cert-manager with Let's Encrypt
4. **Implement backup strategy:** Velero, Azure Backup
5. **Security hardening:** Network policies, Pod Security Standards
6. **Performance tuning:** Resource limits, caching

---

**Status:** ✅ Production-ready deployment configuration complete

**Skills Demonstrated:**
- Infrastructure as Code (Terraform)
- Kubernetes orchestration
- Container management (Docker)
- Azure cloud services
- Production deployment best practices

**Resume bullet:** "Deployed enterprise Django LMS to Azure Kubernetes Service using Terraform IaC, implementing autoscaling (3-10 pods), StatefulSet PostgreSQL, distributed Celery workers, and Azure Files for persistent storage."
