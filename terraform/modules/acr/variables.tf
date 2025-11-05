variable "acr_name" {
  description = "Name of the Azure Container Registry (must be globally unique, alphanumeric only)"
  type        = string
}

variable "location" {
  description = "Azure region for the ACR"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "sku" {
  description = "SKU for ACR (Basic, Standard, Premium)"
  type        = string
  default     = "Standard"
  validation {
    condition     = contains(["Basic", "Standard", "Premium"], var.sku)
    error_message = "SKU must be Basic, Standard, or Premium."
  }
}

variable "admin_enabled" {
  description = "Enable admin user (not recommended for production)"
  type        = bool
  default     = false
}

variable "georeplications" {
  description = "Geo-replication locations for Premium SKU"
  type = list(object({
    location                = string
    zone_redundancy_enabled = bool
  }))
  default = []
}

variable "network_rule_set_enabled" {
  description = "Enable network rule set"
  type        = bool
  default     = false
}

variable "network_rule_default_action" {
  description = "Default action for network rules"
  type        = string
  default     = "Allow"
}

variable "network_rule_ip_rules" {
  description = "List of IP ranges to allow"
  type        = list(string)
  default     = []
}

variable "network_rule_virtual_networks" {
  description = "List of subnet IDs to allow"
  type        = list(string)
  default     = []
}

variable "retention_policy_enabled" {
  description = "Enable retention policy (Premium SKU only)"
  type        = bool
  default     = false
}

variable "retention_policy_days" {
  description = "Number of days to retain untagged manifests"
  type        = number
  default     = 7
}

variable "trust_policy_enabled" {
  description = "Enable content trust policy (Premium SKU only)"
  type        = bool
  default     = false
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
