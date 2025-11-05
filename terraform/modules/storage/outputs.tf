output "storage_account_id" {
  description = "ID of the storage account"
  value       = azurerm_storage_account.storage.id
}

output "storage_account_name" {
  description = "Name of the storage account"
  value       = azurerm_storage_account.storage.name
}

output "storage_account_primary_key" {
  description = "Primary access key for the storage account"
  value       = azurerm_storage_account.storage.primary_access_key
  sensitive   = true
}

output "storage_account_connection_string" {
  description = "Connection string for the storage account"
  value       = azurerm_storage_account.storage.primary_connection_string
  sensitive   = true
}

output "media_share_name" {
  description = "Name of the media file share"
  value       = azurerm_storage_share.media.name
}

output "static_share_name" {
  description = "Name of the static file share"
  value       = azurerm_storage_share.static.name
}

output "backup_container_name" {
  description = "Name of the backup container"
  value       = azurerm_storage_container.backups.name
}
