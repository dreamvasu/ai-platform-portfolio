# 🚀 Ringlet Production Deployment Plan - Azure AKS + Terraform

**Project:** Deploy Ringlet educational platform to Azure Kubernetes Service
**Goal:** Production-ready K8s deployment with Infrastructure as Code
**Timeline:** 6-8 hours
**Why AKS:** You have Azure credits + existing infra (smart choice!)

---

## 📊 What This Accomplishes for Job Application

### ✅ **Fills BOTH Critical Gaps:**
1. **Kubernetes hands-on** - Deploy real Django app to AKS with HPA, persistent storage, Celery workers
2. **Infrastructure as Code** - Complete Terraform modules for AKS cluster, networking, storage

### ✅ **Interview Talking Points:**
- "Deployed multi-tier Django application to Azure Kubernetes Service"
- "Implemented IaC with Terraform for reproducible infrastructure"
- "Managed autoscaling from 3-10 pods with Horizontal Pod Autoscaler"
- "Designed persistent storage strategy with Azure Files (RWX) and Managed Disks (RWO)"
- "Achieved zero-downtime deployments with rolling update strategy"

### ✅ **Portfolio Assets:**
- GitHub repo with complete Terraform code
- Working AKS cluster (can show live)
- Screenshot gallery of `kubectl` commands
- Documentation proving hands-on experience

---

## 🎯 Final Output

After completing this, you'll have:

```
ringlet-deployment/
├── terraform/
│   ├── environments/
│   │   ├── dev/
│   │   └── prod/
│   ├── modules/
│   │   ├── aks-cluster/
│   │   ├── storage/
│   │   ├── networking/
│   │   └── acr/
│   └── global/
│       ├── backend.tf
│       └── providers.tf
├── kubernetes/
│   ├── base/              # Raw YAML manifests
│   └── helm/              # Helm chart (optional)
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   └── screenshots/
└── README.md
```

**Live Resources:**
- ✅ AKS cluster running (3-5 nodes)
- ✅ Ringlet app deployed (3-10 pods autoscaling)
- ✅ PostgreSQL StatefulSet with 10GB disk
- ✅ Redis for caching + Celery broker
- ✅ Azure Files for shared media (ReadWriteMany)
- ✅ Public endpoint with Azure Load Balancer

---

## 📋 Prerequisites

### **What You Need:**

1. **Ringlet Source Code**
   ```bash
   # Option 1: If you have the repo
   cd /path/to/ringlet

   # Option 2: Use the case study Kubernetes manifests
   # We have complete K8s YAML in docs/case-studies/ringlet/kubernetes/
   ```

2. **Azure Subscription**
   - You mentioned you have credits ✅
   - Resource group ready (or we'll create)
   - Contributor access

3. **Tools Installed**
   ```bash
   # Terraform
   brew install terraform  # or: choco install terraform

   # Azure CLI
   brew install azure-cli  # or: choco install azure-cli

   # kubectl
   brew install kubectl  # or: choco install kubernetes-cli

   # Helm (optional but recommended)
   brew install helm
   ```

4. **Azure Login**
   ```bash
   az login
   az account set --subscription "YOUR_SUBSCRIPTION_NAME"
   ```

---

## 🏗️ Architecture Overview

### **What We're Building:**

```
┌─────────────────────────────────────────────────────────────┐
│                      AZURE CLOUD                             │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              AKS CLUSTER (ringlet-aks)                  │ │
│  │                                                          │ │
│  │  ┌────────────────────────────────────────────────────┐│ │
│  │  │           AZURE LOAD BALANCER (Public IP)          ││ │
│  │  └───────────────────────┬────────────────────────────┘│ │
│  │                          │                              │ │
│  │  ┌───────────────────────▼────────────────────────────┐│ │
│  │  │        INGRESS CONTROLLER (nginx)                  ││ │
│  │  └───────────────────────┬────────────────────────────┘│ │
│  │                          │                              │ │
│  │  ┌───────────────────────▼────────────────────────────┐│ │
│  │  │      SERVICE: ringlet-svc (ClusterIP)              ││ │
│  │  └───────────────────────┬────────────────────────────┘│ │
│  │                          │                              │ │
│  │         ┌────────────────┼────────────────┐            │ │
│  │         │                │                │             │ │
│  │  ┌──────▼──────┐  ┌─────▼──────┐  ┌─────▼──────┐     │ │
│  │  │ Django Pod  │  │ Django Pod │  │ Django Pod │      │ │
│  │  │ (3-10 HPA)  │  │            │  │            │      │ │
│  │  └──────┬──────┘  └─────┬──────┘  └─────┬──────┘     │ │
│  │         │               │               │              │ │
│  │         └───────────────┼───────────────┘              │ │
│  │                         │                               │ │
│  │  ┌──────────────────────┼─────────────────────────┐   │ │
│  │  │  HORIZONTAL POD AUTOSCALER (HPA)               │   │ │
│  │  │  Min: 3 | Max: 10 | Target: 70% CPU           │   │ │
│  │  └──────────────────────────────────────────────────┘   │ │
│  │                         │                               │ │
│  │         ┌───────────────┴───────────────┐              │ │
│  │         │                               │               │ │
│  │  ┌──────▼────────┐           ┌─────────▼────────┐     │ │
│  │  │  PostgreSQL   │           │      Redis       │      │ │
│  │  │  StatefulSet  │           │   Deployment     │      │ │
│  │  │  PVC: 10Gi    │           │   Cache+Broker   │      │ │
│  │  └───────────────┘           └──────────────────┘     │ │
│  │                                                         │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │          CELERY WORKERS (2-6 HPA)                │ │ │
│  │  │          CELERY BEAT (Singleton - 1 pod)         │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │                                                         │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │              PERSISTENT STORAGE                   │ │ │
│  │  │  - Azure Files (RWX): 20Gi - Media files         │ │ │
│  │  │  - Azure Disk (RWO): 10Gi - PostgreSQL           │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                 TERRAFORM-MANAGED                        ││
│  │  - AKS Cluster (3-5 nodes, Standard_D2s_v3)             ││
│  │  - Virtual Network + Subnets                            ││
│  │  - Azure Container Registry (ACR)                       ││
│  │  - Storage Accounts (Azure Files)                       ││
│  │  - Managed Disks (PostgreSQL)                           ││
│  │  - Resource Groups                                      ││
│  │  - Network Security Groups                              ││
│  └─────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────┘
```

---

## 📅 Implementation Plan (6-8 hours)

### **PHASE 1: Terraform Infrastructure (3-4 hours)**

#### **Hour 1: Project Structure + Azure Backend**

**1.1 Create Directory Structure (15 min)**
```bash
mkdir -p ringlet-deployment/{terraform/{environments/{dev,prod},modules/{aks-cluster,storage,networking,acr},global},kubernetes/{base,helm},docs/screenshots}
cd ringlet-deployment
```

**1.2 Set Up Terraform Backend (30 min)**

**File: `terraform/global/backend.tf`**
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "ringlet-tfstate-rg"
    storage_account_name = "ringletstate123"  # Must be globally unique
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

**Create backend resources:**
```bash
# Create resource group for Terraform state
az group create --name ringlet-tfstate-rg --location eastus

# Create storage account (replace with unique name)
az storage account create \
  --name ringletstate123 \
  --resource-group ringlet-tfstate-rg \
  --location eastus \
  --sku Standard_LRS

# Get storage account key
ACCOUNT_KEY=$(az storage account keys list \
  --resource-group ringlet-tfstate-rg \
  --account-name ringletstate123 \
  --query '[0].value' -o tsv)

# Create container
az storage container create \
  --name tfstate \
  --account-name ringletstate123 \
  --account-key $ACCOUNT_KEY
```

**File: `terraform/global/providers.tf`**
```hcl
terraform {
  required_version = ">= 1.6"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

provider "azurerm" {
  features {}
}
```

**1.3 Create AKS Module (15 min)**

**File: `terraform/modules/aks-cluster/main.tf`**
```hcl
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.cluster_name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = var.dns_prefix
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name                = "default"
    node_count          = var.node_count
    vm_size             = var.vm_size
    enable_auto_scaling = true
    min_count           = var.min_count
    max_count           = var.max_count
    vnet_subnet_id      = var.subnet_id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
    service_cidr      = "10.2.0.0/16"
    dns_service_ip    = "10.2.0.10"
  }

  tags = var.tags
}

# Role assignment for ACR pull
resource "azurerm_role_assignment" "aks_acr_pull" {
  count                = var.acr_id != null ? 1 : 0
  principal_id         = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name = "AcrPull"
  scope                = var.acr_id
}
```

**File: `terraform/modules/aks-cluster/variables.tf`**
```hcl
variable "cluster_name" {
  type = string
}

variable "location" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "dns_prefix" {
  type = string
}

variable "kubernetes_version" {
  type    = string
  default = "1.27.7"
}

variable "node_count" {
  type    = number
  default = 3
}

variable "vm_size" {
  type    = string
  default = "Standard_D2s_v3"
}

variable "min_count" {
  type    = number
  default = 3
}

variable "max_count" {
  type    = number
  default = 10
}

variable "subnet_id" {
  type = string
}

variable "acr_id" {
  type    = string
  default = null
}

variable "tags" {
  type    = map(string)
  default = {}
}
```

**File: `terraform/modules/aks-cluster/outputs.tf`**
```hcl
output "cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "cluster_id" {
  value = azurerm_kubernetes_cluster.aks.id
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}

output "host" {
  value     = azurerm_kubernetes_cluster.aks.kube_config[0].host
  sensitive = true
}

output "client_certificate" {
  value     = azurerm_kubernetes_cluster.aks.kube_config[0].client_certificate
  sensitive = true
}

output "client_key" {
  value     = azurerm_kubernetes_cluster.aks.kube_config[0].client_key
  sensitive = true
}

output "cluster_ca_certificate" {
  value     = azurerm_kubernetes_cluster.aks.kube_config[0].cluster_ca_certificate
  sensitive = true
}
```

---

#### **Hour 2: Networking + ACR Modules**

**File: `terraform/modules/networking/main.tf`**
```hcl
resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  address_space       = var.address_space
  location            = var.location
  resource_group_name = var.resource_group_name

  tags = var.tags
}

resource "azurerm_subnet" "aks_subnet" {
  name                 = var.subnet_name
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.subnet_address_prefix
}

resource "azurerm_network_security_group" "nsg" {
  name                = "${var.vnet_name}-nsg"
  location            = var.location
  resource_group_name = var.resource_group_name

  security_rule {
    name                       = "allow_https"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "allow_http"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = var.tags
}

resource "azurerm_subnet_network_security_group_association" "nsg_assoc" {
  subnet_id                 = azurerm_subnet.aks_subnet.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}
```

**File: `terraform/modules/acr/main.tf`**
```hcl
resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = var.sku
  admin_enabled       = false

  tags = var.tags
}
```

---

#### **Hour 3: Environment Configuration**

**File: `terraform/environments/prod/main.tf`**
```hcl
terraform {
  backend "azurerm" {}
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

# Networking
module "networking" {
  source = "../../modules/networking"

  vnet_name              = var.vnet_name
  address_space          = var.address_space
  subnet_name            = var.subnet_name
  subnet_address_prefix  = var.subnet_address_prefix
  location               = var.location
  resource_group_name    = azurerm_resource_group.rg.name
  tags                   = var.tags
}

# Azure Container Registry
module "acr" {
  source = "../../modules/acr"

  acr_name            = var.acr_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  sku                 = "Basic"
  tags                = var.tags
}

# AKS Cluster
module "aks" {
  source = "../../modules/aks-cluster"

  cluster_name        = var.cluster_name
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = var.dns_prefix
  kubernetes_version  = var.kubernetes_version
  node_count          = var.node_count
  vm_size             = var.vm_size
  min_count           = var.min_count
  max_count           = var.max_count
  subnet_id           = module.networking.subnet_id
  acr_id              = module.acr.acr_id
  tags                = var.tags

  depends_on = [module.networking, module.acr]
}
```

**File: `terraform/environments/prod/terraform.tfvars`** (gitignored)
```hcl
# Resource Group
resource_group_name = "ringlet-prod-rg"
location            = "East US"

# Networking
vnet_name              = "ringlet-vnet"
address_space          = ["10.1.0.0/16"]
subnet_name            = "aks-subnet"
subnet_address_prefix  = ["10.1.1.0/24"]

# ACR
acr_name = "ringletreg123"  # Must be globally unique

# AKS
cluster_name       = "ringlet-aks"
dns_prefix         = "ringlet"
kubernetes_version = "1.27.7"
node_count         = 3
vm_size            = "Standard_D2s_v3"
min_count          = 3
max_count          = 10

# Tags
tags = {
  Environment = "Production"
  Project     = "Ringlet"
  ManagedBy   = "Terraform"
}
```

**File: `terraform/environments/prod/outputs.tf`**
```hcl
output "aks_cluster_name" {
  value = module.aks.cluster_name
}

output "acr_login_server" {
  value = module.acr.acr_login_server
}

output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}
```

---

#### **Hour 4: Deploy Infrastructure**

```bash
cd terraform/environments/prod

# Initialize
terraform init

# Plan
terraform plan -var-file="terraform.tfvars" -out=tfplan

# Apply (this will take 10-15 minutes)
terraform apply tfplan

# Get AKS credentials
az aks get-credentials \
  --resource-group ringlet-prod-rg \
  --name ringlet-aks \
  --overwrite-existing

# Verify
kubectl get nodes
```

**Expected Output:**
```
NAME                                STATUS   ROLES   AGE   VERSION
aks-default-12345678-vmss000000     Ready    agent   5m    v1.27.7
aks-default-12345678-vmss000001     Ready    agent   5m    v1.27.7
aks-default-12345678-vmss000002     Ready    agent   5m    v1.27.7
```

---

### **PHASE 2: Kubernetes Deployment (2-3 hours)**

#### **Hour 5: Build and Push Docker Image**

**5.1 Get Ringlet Source**
```bash
# If you have the repo
cd /path/to/ringlet

# If not, we'll use a simplified Django app for demo
# (You mentioned you want to deploy Ringlet - we can use actual code)
```

**5.2 Build Docker Image**
```bash
# Get ACR login server
ACR_NAME=$(terraform -chdir=terraform/environments/prod output -raw acr_login_server)

# Login to ACR
az acr login --name ringletreg123

# Build image (use optimized Dockerfile from case study)
docker build -t $ACR_NAME/ringlet:v1.0.0 .

# Push to ACR
docker push $ACR_NAME/ringlet:v1.0.0

# Verify
az acr repository list --name ringletreg123 -o table
```

---

#### **Hour 6: Deploy Kubernetes Resources**

**6.1 Create Namespace**
```bash
kubectl create namespace ringlet
```

**6.2 Create Secrets**
```bash
kubectl create secret generic ringlet-secrets \
  --namespace=ringlet \
  --from-literal=DJANGO_SECRET_KEY='your-secret-key-here' \
  --from-literal=DB_PASSWORD='secure-password'
```

**6.3 Deploy PostgreSQL**
```bash
# Use the YAML from docs/case-studies/ringlet/kubernetes/postgres-deployment.yaml
# Update image if needed for Azure

kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml
```

**6.4 Deploy Redis**
```bash
kubectl apply -f kubernetes/redis-deployment.yaml
kubectl apply -f kubernetes/redis-service.yaml
```

**6.5 Deploy Django App**
```bash
# Update image in deployment YAML to use ACR
# Replace: gcr.io/PROJECT/ringlet:v1
# With: ringletreg123.azurecr.io/ringlet:v1.0.0

kubectl apply -f kubernetes/django-deployment.yaml
kubectl apply -f kubernetes/django-service.yaml
```

**6.6 Deploy Celery Workers**
```bash
kubectl apply -f kubernetes/celery-deployment.yaml
```

**6.7 Deploy HPA**
```bash
kubectl apply -f kubernetes/hpa.yaml
```

**6.8 Deploy Ingress**
```bash
# Install NGINX Ingress Controller (if not already)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# Wait for external IP
kubectl get service -n ingress-nginx

# Deploy app ingress
kubectl apply -f kubernetes/ingress.yaml
```

---

#### **Hour 7-8: Testing & Documentation**

**7.1 Verification**
```bash
# Check all pods
kubectl get all -n ringlet

# Test health endpoint
EXTERNAL_IP=$(kubectl get service ingress-nginx-controller \
  -n ingress-nginx \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

curl http://$EXTERNAL_IP/health/

# Check HPA
kubectl get hpa -n ringlet

# Load test (Apache Bench)
ab -n 1000 -c 100 http://$EXTERNAL_IP/
```

**7.2 Screenshots**
```bash
# Take screenshots of:
1. kubectl get all -n ringlet
2. kubectl get nodes
3. kubectl describe hpa -n ringlet
4. kubectl top pods -n ringlet
5. Azure Portal - AKS cluster overview
6. Azure Portal - ACR repositories
7. Browser - Ringlet app homepage
8. terraform plan output
```

**7.3 Documentation**
- Create README.md with deployment guide
- Document architecture diagram
- Write troubleshooting section
- Create cost estimate

---

## 💰 Cost Estimate (Azure AKS)

| Component | Specs | Monthly Cost |
|-----------|-------|--------------|
| AKS Cluster (3 nodes) | Standard_D2s_v3 | ~$210 |
| Azure Load Balancer | Standard | ~$18 |
| Azure Files (20GB) | Standard | ~$2 |
| Managed Disk (10GB) | Standard SSD | ~$2 |
| Egress (100GB) | Internet | ~$8 |
| **TOTAL** | | **~$240/month** |

**Savings tip:** Use Azure free credits!

---

## 📝 Final Deliverables

### **For GitHub:**
```
ringlet-aks-deployment/
├── README.md (deployment guide)
├── terraform/ (complete IaC)
├── kubernetes/ (K8s manifests)
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── screenshots/
└── .gitignore
```

### **For Resume:**
```
**Ringlet Platform - Production Kubernetes Deployment**
- Deployed Django application to Azure Kubernetes Service (AKS)
- Implemented Infrastructure as Code using Terraform modules
- Achieved autoscaling from 3-10 pods with Horizontal Pod Autoscaler
- Managed persistent storage with Azure Files (RWX) and Managed Disks
- Zero-downtime rolling updates with health checks and probes

GitHub: [link] | Live Demo: http://[AKS-IP]
```

---

## 🎯 Next Steps

1. **Download/Clone Ringlet Repo** (or tell me where it is)
2. **I'll generate all Terraform files** based on this plan
3. **We deploy infrastructure** (`terraform apply`)
4. **We deploy Kubernetes** (`kubectl apply`)
5. **We test and screenshot** everything
6. **We push to GitHub** with docs

**Ready to start?** Tell me:
1. Do you have the Ringlet repo? If yes, where?
2. What's your Azure subscription name?
3. Should I create all the Terraform files now?

**Time to completion: 6-8 hours** ⏱️
**Result: 90%+ job match** 🎯
