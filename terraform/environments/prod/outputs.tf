output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "aks_cluster_name" {
  description = "Name of the AKS cluster"
  value       = module.aks.cluster_name
}

output "aks_cluster_fqdn" {
  description = "FQDN of the AKS cluster"
  value       = module.aks.cluster_fqdn
}

output "acr_login_server" {
  description = "Login server for ACR"
  value       = module.acr.login_server
}

output "storage_account_name" {
  description = "Name of the storage account"
  value       = module.storage.storage_account_name
}

output "kube_config_command" {
  description = "Command to get kubeconfig"
  value       = "az aks get-credentials --resource-group ${azurerm_resource_group.main.name} --name ${module.aks.cluster_name}"
}

output "acr_login_command" {
  description = "Command to login to ACR"
  value       = "az acr login --name ${module.acr.acr_name}"
}

# Sensitive outputs
output "kube_config" {
  description = "Kubeconfig for the AKS cluster"
  value       = module.aks.kube_config
  sensitive   = true
}

output "storage_account_key" {
  description = "Primary key for storage account"
  value       = module.storage.storage_account_primary_key
  sensitive   = true
}
