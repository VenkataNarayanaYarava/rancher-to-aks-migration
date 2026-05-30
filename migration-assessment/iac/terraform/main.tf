terraform {
  required_version = ">= 1.6.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# -------------------------
# Resource Group
# -------------------------
resource "azurerm_resource_group" "rg" {
  name     = "rg-radiant-petclinic"
  location = var.location
}

# -------------------------
# VNet
# -------------------------
resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-radiant-petclinic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.10.0.0/16"]
}

# -------------------------
# AKS Subnet
# -------------------------
resource "azurerm_subnet" "aks_subnet" {
  name                 = "snet-aks"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.10.1.0/24"]
}

# -------------------------
# Log Analytics Workspace
# -------------------------
resource "azurerm_log_analytics_workspace" "law" {
  name                = "law-radiant-petclinic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# -------------------------
# Azure Container Registry
# -------------------------
resource "azurerm_container_registry" "acr" {
  name                = "acrradiantpetclinic00123"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"
  admin_enabled       = false
}

# -------------------------
# AKS Cluster (PRODUCTION-GRADE)
# -------------------------
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-radiant-petclinic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "radiantpetclinic"

  # 🔒 PRIVATE CLUSTER
  private_cluster_enabled = true

  identity {
    type = "SystemAssigned"
  }

  # =========================
  # 🔐 WORKLOAD IDENTITY (MODERN)
  # =========================
  oidc_issuer_enabled       = true
  workload_identity_enabled  = true

  default_node_pool {
    name           = "systempool"
    vm_size        = "Standard_DS2_v2"
    node_count     = 2
    vnet_subnet_id = azurerm_subnet.aks_subnet.id

    type = "VirtualMachineScaleSets"
  }

  # =========================
  # 🌐 NETWORK (Cilium)
  # =========================
  network_profile {
    network_plugin    = "azure"
    network_policy    = "cilium"
    load_balancer_sku = "standard"

    service_cidr   = "10.2.0.0/16"
    dns_service_ip = "10.2.0.10"
  }

  # =========================
  # 📊 AZURE MONITOR (MODERN)
  # =========================
  monitor_metrics {}

  # Logs still go to Log Analytics (Container Insights)
  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
  }
}

# -------------------------
# ACR Pull Access
# -------------------------
resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
}

# -------------------------
# AKS Diagnostic Logs (Control Plane visibility)
# -------------------------
resource "azurerm_monitor_diagnostic_setting" "aks_diag" {
  name                       = "aks-diagnostics"
  target_resource_id         = azurerm_kubernetes_cluster.aks.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id

  enabled_log {
    category = "kube-apiserver"
  }

  enabled_log {
    category = "kube-audit"
  }

  enabled_log {
    category = "kube-scheduler"
  }

  metric {
    category = "AllMetrics"
  }
}