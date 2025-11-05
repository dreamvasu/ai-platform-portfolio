# Storage Module - Azure Files for ReadWriteMany persistent volumes

resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  location                 = var.location
  resource_group_name      = var.resource_group_name
  account_tier             = var.account_tier
  account_replication_type = var.replication_type
  account_kind             = "StorageV2"

  # Enable HTTPS only
  enable_https_traffic_only = true

  # Minimum TLS version
  min_tls_version = "TLS1_2"

  # Network rules
  network_rules {
    default_action             = var.network_default_action
    ip_rules                   = var.network_ip_rules
    virtual_network_subnet_ids = var.network_subnet_ids
    bypass                     = ["AzureServices"]
  }

  # Blob properties (soft delete, versioning)
  blob_properties {
    delete_retention_policy {
      days = var.blob_soft_delete_days
    }

    container_delete_retention_policy {
      days = var.container_soft_delete_days
    }

    versioning_enabled = var.blob_versioning_enabled
  }

  tags = var.tags
}

# Azure File Share for media files (RWX)
resource "azurerm_storage_share" "media" {
  name                 = var.media_share_name
  storage_account_name = azurerm_storage_account.storage.name
  quota                = var.media_share_quota_gb
  enabled_protocol     = "SMB"
}

# Azure File Share for static files (RWX)
resource "azurerm_storage_share" "static" {
  name                 = var.static_share_name
  storage_account_name = azurerm_storage_account.storage.name
  quota                = var.static_share_quota_gb
  enabled_protocol     = "SMB"
}

# Storage Container for backups
resource "azurerm_storage_container" "backups" {
  name                  = var.backup_container_name
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

# Diagnostic settings
resource "azurerm_monitor_diagnostic_setting" "storage" {
  count                      = var.log_analytics_workspace_id != null ? 1 : 0
  name                       = "${var.storage_account_name}-diagnostics"
  target_resource_id         = "${azurerm_storage_account.storage.id}/fileServices/default"
  log_analytics_workspace_id = var.log_analytics_workspace_id

  enabled_log {
    category = "StorageRead"
  }

  enabled_log {
    category = "StorageWrite"
  }

  enabled_log {
    category = "StorageDelete"
  }

  metric {
    category = "Transaction"
    enabled  = true
  }
}
