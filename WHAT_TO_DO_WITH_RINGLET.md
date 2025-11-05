# 🎯 What to Do with Downloaded Ringlet Repo

**Quick guide: Copy deployment files to Ringlet and deploy to Azure AKS**

---

## ✅ Step 1: Copy All Files to Ringlet

### Option A: Use the Copy Script (Recommended)

```bash
# Navigate to ai-platform-portfolio
cd /Users/vasukapoor/Jobs/practice/kub/ai-platform-portfolio

# Run the copy script (replace path with where you downloaded Ringlet)
./copy-to-ringlet.sh ~/Downloads/ringlet

# Example paths:
# ./copy-to-ringlet.sh ~/Downloads/ringlet
# ./copy-to-ringlet.sh ~/Projects/ringlet
# ./copy-to-ringlet.sh /path/to/wherever/you/put/ringlet
```

The script will copy:
- ✅ Terraform infrastructure (16 files)
- ✅ Kubernetes manifests (8 files)
- ✅ Dockerfile + .dockerignore
- ✅ Documentation (4 files)
- ✅ CLAUDE.md for future sessions

### Option B: Manual Copy

```bash
# Set your Ringlet path
RINGLET=/path/to/ringlet

# Copy everything
cp -r terraform/ "$RINGLET/"
cp -r kubernetes/ringlet/ "$RINGLET/kubernetes/"
cp kubernetes/ringlet/Dockerfile "$RINGLET/"
cp kubernetes/ringlet/.dockerignore "$RINGLET/"
cp RINGLET_DEPLOYMENT_GUIDE.md "$RINGLET/"
cp RINGLET_AKS_COMPLETION_STATUS.md "$RINGLET/"
cp RINGLET_CLAUDE.md "$RINGLET/CLAUDE.md"
cp terraform/README.md "$RINGLET/terraform/"
cp kubernetes/ringlet/README.md "$RINGLET/kubernetes/"
```

---

## ⚙️ Step 2: Adjust Files in Ringlet

After copying, navigate to Ringlet:

```bash
cd /path/to/ringlet  # Your Ringlet location
```

### A. Check Django Structure

```bash
# See what Ringlet actually has
ls -la

# Find Django settings
find . -name "settings.py"
find . -name "wsgi.py"

# Check if it uses 'config' or 'ringlet' as project name
ls -la config/ 2>/dev/null || ls -la ringlet/ 2>/dev/null
```

### B. Merge requirements.txt

If Ringlet has existing requirements:

```bash
# Your original requirements were backed up to:
cat requirements.original.txt

# New deployment requirements are in:
cat kubernetes/ringlet/requirements.txt

# Merge them:
nano requirements.txt

# Make sure you have these for production:
# - gunicorn==21.2.0
# - celery==5.3.4
# - redis==5.0.1
# - django-celery-beat==2.5.0
```

### C. Update Dockerfile

```bash
nano Dockerfile

# Find this line near the end:
CMD ["gunicorn", ... "config.wsgi:application"]

# Change to match your Django structure:
# If Ringlet uses 'ringlet' instead of 'config':
CMD ["gunicorn", ... "ringlet.wsgi:application"]

# Also check DJANGO_SETTINGS_MODULE if you set it:
ENV DJANGO_SETTINGS_MODULE="ringlet.settings.production"
```

### D. Update ConfigMap

```bash
nano kubernetes/base/configmap.yaml

# Update these to match Ringlet:
data:
  DJANGO_SETTINGS_MODULE: "ringlet.settings.production"  # or config.settings.production
  # Add any Ringlet-specific env vars here
```

### E. Create Health Check Endpoint

Ringlet needs a `/health/` endpoint for Kubernetes probes.

Create or update `config/urls.py` (or `ringlet/urls.py`):

```python
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
    # ... rest of your URLs
]
```

---

## 🚀 Step 3: Deploy to Azure

Now follow the deployment guide:

```bash
cd /path/to/ringlet

# Read the guide
cat RINGLET_DEPLOYMENT_GUIDE.md

# Or jump straight in:
cd terraform/environments/prod
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars  # Fill in your values
```

**Follow these phases from RINGLET_DEPLOYMENT_GUIDE.md:**

1. **Phase 1:** Provision infrastructure with Terraform (3-4 hours)
2. **Phase 2:** Build and push Docker image (1 hour)
3. **Phase 3:** Deploy to Kubernetes (2-3 hours)
4. **Phase 4:** Configure ingress (optional)

---

## 📚 Important Files in Ringlet

After copying, your Ringlet repo will have:

### **Root Directory**
```
ringlet/
├── CLAUDE.md                           ← Guide for Claude Code
├── RINGLET_DEPLOYMENT_GUIDE.md         ← Complete deployment guide
├── RINGLET_AKS_COMPLETION_STATUS.md    ← What you achieved
├── RINGLET_SETUP_GUIDE.md              ← This guide
├── Dockerfile                          ← Production Docker build
├── .dockerignore                       ← Build optimization
├── requirements.txt                    ← Python dependencies
```

### **Terraform Infrastructure**
```
terraform/
├── README.md                           ← Terraform documentation
├── modules/
│   ├── networking/                     ← VNet, subnets, NSGs
│   ├── aks-cluster/                    ← AKS configuration
│   ├── acr/                            ← Container registry
│   └── storage/                        ← Azure Files
└── environments/
    └── prod/
        ├── main.tf                     ← Main configuration
        ├── variables.tf                ← Input variables
        ├── outputs.tf                  ← Output values
        └── terraform.tfvars.example    ← Template to copy
```

### **Kubernetes Manifests**
```
kubernetes/
├── README.md                           ← K8s documentation
└── base/
    ├── postgres-statefulset.yaml       ← Database
    ├── redis-deployment.yaml           ← Cache
    ├── django-deployment.yaml          ← Web app
    ├── django-hpa.yaml                 ← Autoscaling
    ├── celery-worker-deployment.yaml   ← Workers
    ├── celery-beat-deployment.yaml     ← Scheduler
    ├── configmap.yaml                  ← Configuration
    └── ingress.yaml                    ← Load balancer
```

---

## 🎯 Quick Start Commands

Once files are copied and adjusted:

```bash
cd /path/to/ringlet

# 1. Setup Terraform backend (one-time)
# Follow RINGLET_DEPLOYMENT_GUIDE.md Step 1

# 2. Deploy infrastructure
cd terraform/environments/prod
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# 3. Build Docker image
cd ../..  # Back to Ringlet root
az acr login --name ringletprodacr
docker build -t ringletprodacr.azurecr.io/ringlet:latest .
docker push ringletprodacr.azurecr.io/ringlet:latest

# 4. Deploy to Kubernetes
az aks get-credentials --resource-group ringlet-prod-rg --name ringlet-prod-aks
kubectl apply -f kubernetes/base/
kubectl get pods -n ringlet -w

# 5. Test
kubectl port-forward svc/django 8000:8000 -n ringlet
curl http://localhost:8000/health/
```

---

## 📋 Checklist

Before deploying:

- [ ] Copied all files to Ringlet repo
- [ ] Checked Django structure (config vs ringlet)
- [ ] Merged requirements.txt
- [ ] Updated Dockerfile WSGI path
- [ ] Updated ConfigMap settings module
- [ ] Created `/health/` endpoint
- [ ] Installed Azure CLI (`az --version`)
- [ ] Installed Terraform (`terraform --version`)
- [ ] Installed kubectl (`kubectl version`)
- [ ] Logged into Azure (`az login`)
- [ ] Read RINGLET_DEPLOYMENT_GUIDE.md

After deployment:

- [ ] Infrastructure provisioned (Terraform)
- [ ] Docker image built and pushed
- [ ] Kubernetes resources deployed
- [ ] All pods running (`kubectl get pods -n ringlet`)
- [ ] Health check passing
- [ ] Migrations run
- [ ] Superuser created
- [ ] Can access application

---

## 🆘 Need Help?

### In Future Claude Code Sessions

Just say: **"Help me deploy Ringlet to AKS"**

Claude will read `CLAUDE.md` in the Ringlet repo and know exactly what to do.

### Documentation References

1. **RINGLET_DEPLOYMENT_GUIDE.md** - Step-by-step deployment
2. **terraform/README.md** - Terraform module docs
3. **kubernetes/README.md** - Kubernetes deployment docs
4. **CLAUDE.md** - Project overview and common tasks

---

## 🎉 What You're About to Deploy

**Production-ready Django LMS on Azure AKS:**

- ✅ Terraform Infrastructure as Code (4 modules)
- ✅ Kubernetes with autoscaling (3-10 Django pods, 2-6 Celery workers)
- ✅ StatefulSet PostgreSQL with persistent storage
- ✅ Redis cache with AOF persistence
- ✅ Multi-stage Docker build (optimized + secure)
- ✅ Azure Files for shared media/static
- ✅ Horizontal Pod Autoscaling (HPA)
- ✅ Health checks and rolling updates
- ✅ Complete monitoring and logging

**This proves you can:**
- Deploy production applications to Kubernetes ✅
- Write Infrastructure as Code with Terraform ✅
- Design scalable architectures ✅
- Follow cloud best practices ✅

---

## 🚀 Let's Go!

```bash
# Copy files to Ringlet
./copy-to-ringlet.sh /path/to/ringlet

# Navigate to Ringlet
cd /path/to/ringlet

# Start reading
cat RINGLET_DEPLOYMENT_GUIDE.md

# Or jump straight to deployment
cd terraform/environments/prod
```

**Good luck with the deployment! 🎯**
