variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "eastus"
}

variable "owner" {
  description = "Owner/creator of the resources"
  type        = string
  default     = "vasu-kapoor"
}

variable "cost_center" {
  description = "Cost center for billing"
  type        = string
  default     = "learning-sprint"
}

# Networking Variables
variable "vnet_address_space" {
  description = "Address space for the VNet"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "aks_subnet_address_prefix" {
  description = "Address prefix for AKS subnet"
  type        = list(string)
  default     = ["10.0.1.0/24"]
}

variable "postgres_subnet_address_prefix" {
  description = "Address prefix for PostgreSQL subnet"
  type        = list(string)
  default     = ["10.0.2.0/24"]
}

# ACR Variables
variable "acr_sku" {
  description = "SKU for Azure Container Registry"
  type        = string
  default     = "Standard"
}

# Storage Variables
variable "storage_replication_type" {
  description = "Storage replication type"
  type        = string
  default     = "LRS"
}

variable "media_storage_quota_gb" {
  description = "Quota in GB for media file share"
  type        = number
  default     = 50
}

variable "static_storage_quota_gb" {
  description = "Quota in GB for static file share"
  type        = number
  default     = 10
}

# AKS Variables
variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28"
}

variable "aks_system_node_count" {
  description = "Initial node count for system pool"
  type        = number
  default     = 1
}

variable "aks_system_vm_size" {
  description = "VM size for system node pool"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "aks_system_min_count" {
  description = "Minimum nodes for system pool"
  type        = number
  default     = 1
}

variable "aks_system_max_count" {
  description = "Maximum nodes for system pool"
  type        = number
  default     = 3
}

variable "aks_user_vm_size" {
  description = "VM size for user node pool"
  type        = string
  default     = "Standard_D4s_v3"
}

variable "aks_user_min_count" {
  description = "Minimum nodes for user pool"
  type        = number
  default     = 2
}

variable "aks_user_max_count" {
  description = "Maximum nodes for user pool"
  type        = number
  default     = 6
}

variable "aks_admin_group_object_ids" {
  description = "Azure AD group object IDs for AKS admins"
  type        = list(string)
  default     = []
}

# Database Variables
variable "postgres_user" {
  description = "PostgreSQL username"
  type        = string
  default     = "ringlet"
  sensitive   = true
}

variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "postgres_db" {
  description = "PostgreSQL database name"
  type        = string
  default     = "ringlet_prod"
}
