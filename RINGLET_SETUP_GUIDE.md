# 🚀 Setting Up Ringlet with Kubernetes + Terraform

**Guide to copy deployment files from ai-platform-portfolio to Ringlet repo**

---

## 📂 Step 1: Copy Files to Ringlet Repository

Assuming Ringlet is downloaded to: `/path/to/ringlet`

### Copy Command (run from ai-platform-portfolio)

```bash
# Set Ringlet path (UPDATE THIS!)
RINGLET_PATH="/path/to/ringlet"  # e.g., ~/Downloads/ringlet

# Navigate to ai-platform-portfolio
cd /Users/vasukapoor/Jobs/practice/kub/ai-platform-portfolio

# Copy Terraform infrastructure
cp -r terraform/ "$RINGLET_PATH/"

# Copy Kubernetes manifests
cp -r kubernetes/ringlet/ "$RINGLET_PATH/kubernetes/"

# Copy Docker files (to root of Ringlet)
cp kubernetes/ringlet/Dockerfile "$RINGLET_PATH/"
cp kubernetes/ringlet/.dockerignore "$RINGLET_PATH/"

# Copy deployment documentation
cp RINGLET_DEPLOYMENT_GUIDE.md "$RINGLET_PATH/"
cp RINGLET_AKS_COMPLETION_STATUS.md "$RINGLET_PATH/"

# Copy README files
cp terraform/README.md "$RINGLET_PATH/terraform/"
cp kubernetes/ringlet/README.md "$RINGLET_PATH/kubernetes/"
```

---

## 📋 Step 2: What Gets Copied

### Into Ringlet Root Directory
```
ringlet/
├── Dockerfile                    ← FROM kubernetes/ringlet/Dockerfile
├── .dockerignore                 ← FROM kubernetes/ringlet/.dockerignore
├── RINGLET_DEPLOYMENT_GUIDE.md   ← Deployment guide
├── RINGLET_AKS_COMPLETION_STATUS.md
└── CLAUDE.md                     ← Will be created
```

### Terraform Infrastructure
```
ringlet/terraform/
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── aks-cluster/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── acr/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── storage/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── terraform.tfvars.example
└── README.md
```

### Kubernetes Manifests
```
ringlet/kubernetes/
├── base/
│   ├── postgres-statefulset.yaml
│   ├── redis-deployment.yaml
│   ├── django-deployment.yaml
│   ├── django-hpa.yaml
│   ├── celery-worker-deployment.yaml
│   ├── celery-beat-deployment.yaml
│   ├── configmap.yaml
│   └── ingress.yaml
└── README.md
```

---

## ⚙️ Step 3: Adjust Files in Ringlet

### 3.1 Update requirements.txt

The copied `requirements.txt` is generic. **Merge it with Ringlet's existing requirements:**

```bash
cd "$RINGLET_PATH"

# If Ringlet has requirements.txt, merge them
cat requirements.txt > requirements.original.txt
cat kubernetes/ringlet/requirements.txt >> requirements.txt

# Remove duplicates manually
nano requirements.txt
```

**Keep all existing Ringlet dependencies, add these if missing:**
```txt
# Production server
gunicorn==21.2.0

# Async tasks
celery==5.3.4
redis==5.0.1
django-celery-beat==2.5.0

# Monitoring
requests==2.31.0
```

### 3.2 Update Dockerfile

The Dockerfile assumes standard Django structure. **Verify these paths match Ringlet:**

```bash
cd "$RINGLET_PATH"
nano Dockerfile
```

**Check:**
- WSGI application path: `config.wsgi:application` or `ringlet.wsgi:application`?
- Settings module: Does Ringlet use `config.settings`?
- Static/media directories: Where are they in Ringlet?

**Common changes needed:**
```dockerfile
# Change this line if Ringlet's WSGI is different
CMD ["gunicorn", "ringlet.wsgi:application"]  # Instead of config.wsgi

# Or if using different settings module
ENV DJANGO_SETTINGS_MODULE="ringlet.settings.production"
```

### 3.3 Update ConfigMap

```bash
cd "$RINGLET_PATH/kubernetes/base"
nano configmap.yaml
```

**Update these based on Ringlet's actual structure:**
```yaml
data:
  # Check what Ringlet actually uses:
  DJANGO_SETTINGS_MODULE: "ringlet.settings.production"  # Or config.settings.production

  # Add any Ringlet-specific environment variables
  # Example: If Ringlet uses S3, add AWS settings
```

### 3.4 Update Django Deployment Image Reference

```bash
nano kubernetes/base/django-deployment.yaml
nano kubernetes/base/celery-worker-deployment.yaml
nano kubernetes/base/celery-beat-deployment.yaml
```

**Change image name if needed:**
```yaml
# If you want different naming:
image: ringletprodacr.azurecr.io/ringlet-lms:latest
# Instead of just "ringlet"
```

---

## 🔧 Step 4: Verify Ringlet Structure

Check what Ringlet actually has:

```bash
cd "$RINGLET_PATH"

# Check project structure
ls -la

# Find Django settings
find . -name "settings.py" -o -name "wsgi.py"

# Check if manage.py exists
ls manage.py

# Check existing requirements
cat requirements.txt
```

**Expected Ringlet structure:**
```
ringlet/
├── manage.py
├── config/  (or ringlet/)
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── wsgi.py
│   └── urls.py
├── apps/
│   ├── courses/
│   ├── users/
│   └── ...
├── requirements.txt
└── ...
```

---

## 🎯 Step 5: Create CLAUDE.md for Ringlet

I'll create this next - it will guide future Claude sessions on how to work with Ringlet.

---

## ✅ Quick Copy Script

Save this as `copy-to-ringlet.sh`:

```bash
#!/bin/bash

# EDIT THIS PATH!
RINGLET_PATH="$HOME/path/to/ringlet"

if [ ! -d "$RINGLET_PATH" ]; then
  echo "❌ Ringlet path not found: $RINGLET_PATH"
  echo "Edit this script and set RINGLET_PATH correctly"
  exit 1
fi

echo "📦 Copying deployment files to Ringlet..."

# Create directories
mkdir -p "$RINGLET_PATH/terraform"
mkdir -p "$RINGLET_PATH/kubernetes"

# Copy Terraform
cp -r terraform/ "$RINGLET_PATH/"
echo "✅ Terraform copied"

# Copy Kubernetes
cp -r kubernetes/ringlet/ "$RINGLET_PATH/kubernetes/"
echo "✅ Kubernetes manifests copied"

# Copy Docker files
cp kubernetes/ringlet/Dockerfile "$RINGLET_PATH/"
cp kubernetes/ringlet/.dockerignore "$RINGLET_PATH/"
echo "✅ Docker files copied"

# Copy docs
cp RINGLET_DEPLOYMENT_GUIDE.md "$RINGLET_PATH/"
cp RINGLET_AKS_COMPLETION_STATUS.md "$RINGLET_PATH/"
echo "✅ Documentation copied"

# Copy READMEs
cp terraform/README.md "$RINGLET_PATH/terraform/"
cp kubernetes/ringlet/README.md "$RINGLET_PATH/kubernetes/"
echo "✅ READMEs copied"

echo ""
echo "🎉 All files copied to: $RINGLET_PATH"
echo ""
echo "📋 Next steps:"
echo "1. cd $RINGLET_PATH"
echo "2. Review and merge requirements.txt"
echo "3. Update Dockerfile WSGI path if needed"
echo "4. Read RINGLET_DEPLOYMENT_GUIDE.md"
echo "5. Deploy! 🚀"
```

Make executable:
```bash
chmod +x copy-to-ringlet.sh
./copy-to-ringlet.sh
```

---

## 📝 Files You'll Need to Modify

After copying, you'll likely need to adjust:

1. **requirements.txt** - Merge with existing Ringlet requirements
2. **Dockerfile** - Update WSGI path to match Ringlet's structure
3. **kubernetes/base/configmap.yaml** - Add Ringlet-specific env vars
4. **kubernetes/base/django-deployment.yaml** - Update health check path if needed

---

## 🚀 After Copying

1. Navigate to Ringlet repo
2. Review copied files
3. Make adjustments listed above
4. Follow RINGLET_DEPLOYMENT_GUIDE.md
5. Deploy to Azure! 🎉

---

**Next:** I'll create CLAUDE.md for the Ringlet repository
