variable "cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
}

variable "location" {
  description = "Azure region for the cluster"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "dns_prefix" {
  description = "DNS prefix for the cluster"
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28"
}

variable "subnet_id" {
  description = "ID of the subnet for AKS"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "system_node_count" {
  description = "Initial node count for system pool"
  type        = number
  default     = 1
}

variable "system_vm_size" {
  description = "VM size for system node pool"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "system_min_count" {
  description = "Minimum nodes for system pool autoscaling"
  type        = number
  default     = 1
}

variable "system_max_count" {
  description = "Maximum nodes for system pool autoscaling"
  type        = number
  default     = 3
}

variable "user_vm_size" {
  description = "VM size for user node pool"
  type        = string
  default     = "Standard_D4s_v3"
}

variable "user_min_count" {
  description = "Minimum nodes for user pool autoscaling"
  type        = number
  default     = 2
}

variable "user_max_count" {
  description = "Maximum nodes for user pool autoscaling"
  type        = number
  default     = 6
}

variable "acr_id" {
  description = "ID of the Azure Container Registry"
  type        = string
}

variable "admin_group_object_ids" {
  description = "Azure AD group object IDs for cluster admins"
  type        = list(string)
  default     = []
}

variable "log_analytics_workspace_id" {
  description = "ID of Log Analytics Workspace (optional, will create if not provided)"
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
