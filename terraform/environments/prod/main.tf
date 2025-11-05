# Production Environment - Ringlet LMS on Azure AKS

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
  }

  # Remote state backend - configure after initial setup
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstateringlet"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }
}

# Local variables
locals {
  environment = "prod"
  project     = "ringlet"
  location    = var.location

  common_tags = {
    Environment = local.environment
    Project     = local.project
    ManagedBy   = "Terraform"
    Owner       = var.owner
    CostCenter  = var.cost_center
  }
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${local.project}-${local.environment}-rg"
  location = local.location
  tags     = local.common_tags
}

# Networking Module
module "networking" {
  source = "../../modules/networking"

  vnet_name                     = "${local.project}-${local.environment}-vnet"
  location                      = azurerm_resource_group.main.location
  resource_group_name           = azurerm_resource_group.main.name
  vnet_address_space            = var.vnet_address_space
  aks_subnet_name               = "aks-subnet"
  aks_subnet_address_prefix     = var.aks_subnet_address_prefix
  postgres_subnet_name          = "postgres-subnet"
  postgres_subnet_address_prefix = var.postgres_subnet_address_prefix

  tags = local.common_tags
}

# Azure Container Registry Module
module "acr" {
  source = "../../modules/acr"

  acr_name            = "${local.project}${local.environment}acr"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = var.acr_sku
  admin_enabled       = false

  tags = local.common_tags
}

# Storage Module
module "storage" {
  source = "../../modules/storage"

  storage_account_name = "${local.project}${local.environment}storage"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  account_tier         = "Standard"
  replication_type     = var.storage_replication_type

  media_share_name     = "media"
  media_share_quota_gb = var.media_storage_quota_gb
  static_share_name    = "static"
  static_share_quota_gb = var.static_storage_quota_gb

  network_subnet_ids = [module.networking.aks_subnet_id]

  tags = local.common_tags
}

# AKS Cluster Module
module "aks" {
  source = "../../modules/aks-cluster"

  cluster_name        = "${local.project}-${local.environment}-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${local.project}-${local.environment}"
  kubernetes_version  = var.kubernetes_version
  subnet_id           = module.networking.aks_subnet_id
  environment         = local.environment

  # System node pool
  system_node_count = var.aks_system_node_count
  system_vm_size    = var.aks_system_vm_size
  system_min_count  = var.aks_system_min_count
  system_max_count  = var.aks_system_max_count

  # User node pool
  user_vm_size    = var.aks_user_vm_size
  user_min_count  = var.aks_user_min_count
  user_max_count  = var.aks_user_max_count

  # ACR integration
  acr_id = module.acr.acr_id

  # Azure AD admin groups
  admin_group_object_ids = var.aks_admin_group_object_ids

  log_analytics_workspace_id = null

  tags = local.common_tags

  depends_on = [
    module.networking,
    module.acr
  ]
}

# Kubernetes Provider Configuration
provider "kubernetes" {
  host                   = module.aks.cluster_fqdn
  client_certificate     = base64decode(module.aks.kube_config[0].client_certificate)
  client_key             = base64decode(module.aks.kube_config[0].client_key)
  cluster_ca_certificate = base64decode(module.aks.kube_config[0].cluster_ca_certificate)
}

# Create namespace for Ringlet
resource "kubernetes_namespace" "ringlet" {
  metadata {
    name = "ringlet"
    labels = {
      environment = local.environment
      project     = local.project
    }
  }

  depends_on = [module.aks]
}

# Create secret for Azure File storage credentials
resource "kubernetes_secret" "azure_file" {
  metadata {
    name      = "azure-file-secret"
    namespace = kubernetes_namespace.ringlet.metadata[0].name
  }

  data = {
    azurestorageaccountname = module.storage.storage_account_name
    azurestorageaccountkey  = module.storage.storage_account_primary_key
  }

  type = "Opaque"

  depends_on = [kubernetes_namespace.ringlet]
}

# Create secret for database credentials
resource "kubernetes_secret" "database" {
  metadata {
    name      = "database-secret"
    namespace = kubernetes_namespace.ringlet.metadata[0].name
  }

  data = {
    POSTGRES_USER     = var.postgres_user
    POSTGRES_PASSWORD = var.postgres_password
    POSTGRES_DB       = var.postgres_db
  }

  type = "Opaque"

  depends_on = [kubernetes_namespace.ringlet]
}
