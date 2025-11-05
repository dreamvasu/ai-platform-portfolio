variable "storage_account_name" {
  description = "Name of the storage account (must be globally unique, lowercase alphanumeric)"
  type        = string
}

variable "location" {
  description = "Azure region for the storage account"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "account_tier" {
  description = "Storage account tier (Standard or Premium)"
  type        = string
  default     = "Standard"
}

variable "replication_type" {
  description = "Storage replication type (LRS, GRS, RAGRS, ZRS)"
  type        = string
  default     = "LRS"
}

variable "network_default_action" {
  description = "Default action for network rules"
  type        = string
  default     = "Allow"
}

variable "network_ip_rules" {
  description = "List of IP addresses to allow"
  type        = list(string)
  default     = []
}

variable "network_subnet_ids" {
  description = "List of subnet IDs to allow"
  type        = list(string)
  default     = []
}

variable "blob_soft_delete_days" {
  description = "Number of days to retain soft-deleted blobs"
  type        = number
  default     = 7
}

variable "container_soft_delete_days" {
  description = "Number of days to retain soft-deleted containers"
  type        = number
  default     = 7
}

variable "blob_versioning_enabled" {
  description = "Enable blob versioning"
  type        = bool
  default     = false
}

variable "media_share_name" {
  description = "Name of the Azure File Share for media files"
  type        = string
  default     = "media"
}

variable "media_share_quota_gb" {
  description = "Quota in GB for media file share"
  type        = number
  default     = 50
}

variable "static_share_name" {
  description = "Name of the Azure File Share for static files"
  type        = string
  default     = "static"
}

variable "static_share_quota_gb" {
  description = "Quota in GB for static file share"
  type        = number
  default     = 10
}

variable "backup_container_name" {
  description = "Name of the blob container for backups"
  type        = string
  default     = "backups"
}

variable "log_analytics_workspace_id" {
  description = "ID of Log Analytics Workspace for diagnostics"
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
