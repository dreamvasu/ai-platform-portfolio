# 🏗️ Terraform Infrastructure for Ringlet AKS

**Production-grade Infrastructure as Code for deploying Ringlet LMS on Azure Kubernetes Service**

---

## 📁 Structure

```
terraform/
├── modules/                    # Reusable Terraform modules
│   ├── aks-cluster/           # AKS cluster with dual node pools
│   ├── acr/                   # Azure Container Registry
│   ├── networking/            # VNet, subnets, NSGs
│   └── storage/               # Azure Files for persistent storage
│
└── environments/              # Environment-specific configurations
    ├── dev/                   # Development (smaller, cheaper)
    └── prod/                  # Production (HA, autoscaling)
```

---

## 🎯 What Gets Created

### Networking
- **Virtual Network** (10.0.0.0/16)
  - AKS subnet (10.0.1.0/24) with service endpoints
  - PostgreSQL subnet (10.0.2.0/24) with delegation
  - Network Security Group with HTTP/HTTPS rules

### Compute (AKS)
- **AKS Cluster** (Kubernetes 1.28+)
  - System node pool: 1-3 nodes (Standard_D2s_v3)
  - User node pool: 2-6 nodes (Standard_D4s_v3)
  - Azure CNI networking
  - Azure RBAC integration
  - Log Analytics monitoring
  - Auto-upgrade enabled

### Container Registry
- **Azure Container Registry** (Standard SKU)
  - Integrated with AKS (AcrPull role)
  - Diagnostic logging
  - Optional geo-replication (Premium SKU)

### Storage
- **Storage Account** (Standard LRS)
  - Azure Files share for media (50GB, RWX)
  - Azure Files share for static (10GB, RWX)
  - Blob container for backups
  - Soft delete enabled (7 days)

### Kubernetes Resources
- **Namespace:** ringlet
- **Secrets:** Database credentials, Azure Files credentials
- **ConfigMaps:** Application configuration

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install tools
brew install terraform azure-cli kubectl

# Login to Azure
az login

# Set subscription
az account set --subscription "YOUR_SUBSCRIPTION_NAME"
```

### Deploy Production Environment

```bash
# 1. Create Terraform backend
./scripts/setup-backend.sh

# 2. Navigate to environment
cd environments/prod

# 3. Configure variables
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars  # Update values

# 4. Initialize Terraform
terraform init

# 5. Plan deployment
terraform plan -out=tfplan

# 6. Apply (takes ~15-20 minutes)
terraform apply tfplan

# 7. Configure kubectl
az aks get-credentials \
  --resource-group $(terraform output -raw resource_group_name) \
  --name $(terraform output -raw aks_cluster_name)

# 8. Verify
kubectl get nodes
terraform output
```

---

## 📝 Module Documentation

### AKS Cluster Module

**Location:** `modules/aks-cluster/`

**Features:**
- Dual node pools (system + user)
- Horizontal autoscaling
- Azure RBAC integration
- Log Analytics monitoring
- Automatic channel upgrades
- Maintenance windows

**Key Variables:**
```hcl
cluster_name        = "ringlet-prod-aks"
kubernetes_version  = "1.28"
system_vm_size      = "Standard_D2s_v3"  # 2 vCPU, 8GB RAM
user_vm_size        = "Standard_D4s_v3"  # 4 vCPU, 16GB RAM
system_min_count    = 1
system_max_count    = 3
user_min_count      = 2
user_max_count      = 6
```

### Networking Module

**Location:** `modules/networking/`

**Features:**
- VNet with customizable address space
- Subnets for AKS and databases
- Service endpoints (SQL, Storage, ACR)
- PostgreSQL subnet delegation
- Network Security Groups

**Key Variables:**
```hcl
vnet_address_space            = ["10.0.0.0/16"]
aks_subnet_address_prefix     = ["10.0.1.0/24"]
postgres_subnet_address_prefix = ["10.0.2.0/24"]
```

### ACR Module

**Location:** `modules/acr/`

**Features:**
- Private container registry
- Integrated with AKS
- Diagnostic logging
- Optional geo-replication
- Image retention policies

**Key Variables:**
```hcl
acr_name = "ringletprodacr"  # Must be globally unique
sku      = "Standard"        # Basic, Standard, or Premium
```

### Storage Module

**Location:** `modules/storage/`

**Features:**
- Azure Files for ReadWriteMany volumes
- Blob storage for backups
- Soft delete protection
- Network restrictions
- Diagnostic logging

**Key Variables:**
```hcl
storage_account_name  = "ringletprodstorage"  # Must be unique
media_share_quota_gb  = 50
static_share_quota_gb = 10
```

---

## 🔧 Configuration

### Environment Variables

Copy and customize:

```bash
cd environments/prod
cp terraform.tfvars.example terraform.tfvars
```

**Required Variables:**
```hcl
# Basic
location    = "eastus"
owner       = "your-name"
cost_center = "project-name"

# Database (IMPORTANT!)
postgres_password = "GENERATE_STRONG_PASSWORD"

# Optional
aks_admin_group_object_ids = ["your-azure-ad-group-id"]
```

### Backend Configuration

Store Terraform state in Azure Storage:

```hcl
# In environments/prod/main.tf
backend "azurerm" {
  resource_group_name  = "terraform-state-rg"
  storage_account_name = "tfstateringlet"
  container_name       = "tfstate"
  key                  = "prod.terraform.tfstate"
}
```

---

## 📊 Outputs

After `terraform apply`, you'll get:

```hcl
resource_group_name    # Azure resource group name
aks_cluster_name       # AKS cluster name
aks_cluster_fqdn       # Cluster FQDN
acr_login_server       # ACR URL for docker push
storage_account_name   # Storage account name
kube_config_command    # Command to get credentials
acr_login_command      # Command to login to ACR
```

**Sensitive outputs:**
```hcl
kube_config           # Kubernetes config (use: terraform output -raw kube_config)
storage_account_key   # Storage account key
```

---

## 💰 Cost Estimation

### Production Environment (~$405-1,105/month)

```
Component                        Cost
-----------------------------------------
AKS Control Plane                FREE
System Pool (1-3 D2s_v3)         $70-210
User Pool (2-6 D4s_v3)           $280-840
Azure Container Registry         $20
Azure Files (60GB)               $12
Managed Disks (25GB)             $3
Load Balancer                    $20
Egress (100GB)                   Variable
```

### Cost Optimization

**Development Environment:**
```hcl
# In environments/dev/terraform.tfvars
aks_system_vm_size = "Standard_B2s"   # $30/month
aks_user_vm_size   = "Standard_B2ms"  # $60/month
system_min_count   = 1
user_min_count     = 1
```

**Stop/Start Cluster:**
```bash
# Stop when not in use
az aks stop --name ringlet-prod-aks --resource-group ringlet-prod-rg

# Start when needed
az aks start --name ringlet-prod-aks --resource-group ringlet-prod-rg
```

---

## 🔒 Security Best Practices

### Implemented
✅ System-assigned managed identity for AKS
✅ Azure RBAC for cluster access
✅ Network security groups
✅ Private endpoints for storage
✅ Non-root container user
✅ Secret management with Kubernetes secrets
✅ TLS 1.2 minimum for storage

### Recommended Additions
- [ ] Azure Key Vault for secrets
- [ ] Azure Policy for governance
- [ ] Private AKS cluster
- [ ] Network policies in Kubernetes
- [ ] Pod Security Standards

---

## 🧪 Validation

### Verify Terraform

```bash
# Validate syntax
terraform validate

# Format code
terraform fmt -recursive

# Plan without applying
terraform plan

# Show current state
terraform show
```

### Verify Infrastructure

```bash
# Check AKS
az aks show --name ringlet-prod-aks --resource-group ringlet-prod-rg

# Check ACR
az acr list --resource-group ringlet-prod-rg --output table

# Check storage
az storage account show --name ringletprodstorage

# Check networking
az network vnet list --resource-group ringlet-prod-rg --output table
```

---

## 🔄 Update Infrastructure

### Modify Configuration

```bash
# Edit variables
nano terraform.tfvars

# Plan changes
terraform plan -out=tfplan

# Review plan carefully
terraform show tfplan

# Apply if looks good
terraform apply tfplan
```

### Upgrade Kubernetes Version

```bash
# Check available versions
az aks get-versions --location eastus --output table

# Update variable
# kubernetes_version = "1.29"

# Plan and apply
terraform plan -out=tfplan
terraform apply tfplan
```

---

## 🧹 Cleanup

### Destroy Everything

```bash
# CAREFUL: This deletes all resources!
cd environments/prod
terraform destroy

# Type "yes" to confirm
```

### Partial Cleanup

```bash
# Delete specific resource
terraform destroy -target=module.aks

# Keep everything else
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Backend initialization fails**
```bash
# Create backend manually
./scripts/setup-backend.sh

# Or initialize without backend
terraform init -backend=false
```

**2. Resource name conflicts**
```bash
# ACR and Storage names must be globally unique
# Try adding random suffix:
acr_name = "ringlet${random_string.suffix.result}acr"
```

**3. Permission errors**
```bash
# Ensure you have Contributor role
az role assignment list --assignee $(az account show --query user.name -o tsv)
```

**4. Plan fails with cycle errors**
```bash
# Usually dependency issue in modules
# Check depends_on blocks in main.tf
```

### Debug Mode

```bash
# Enable detailed logging
export TF_LOG=DEBUG
terraform plan

# Or specific component
export TF_LOG_PROVIDER=DEBUG
```

---

## 📚 Additional Resources

- [Terraform Azure Provider Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [AKS Best Practices](https://learn.microsoft.com/en-us/azure/aks/best-practices)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

---

**Created:** November 2, 2025
**Author:** Vasu Kapoor
**Purpose:** Learning sprint - Kubernetes + Terraform hands-on experience
