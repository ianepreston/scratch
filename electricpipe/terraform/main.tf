terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      # Root module should specify the maximum provider version
      # The ~> operator is a convenient shorthand for allowing only patch releases within a specific minor release.
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}


data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "resource_group" {
  name     = "${var.project}-${var.environment}-resource-group"
  location = var.location
}

resource "azurerm_application_insights" "application_insights" {
  name                = "${var.project}-${var.environment}-application-insights"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name
  application_type    = "web"
}
resource "azurerm_storage_account" "storage_account" {
  name                     = "${var.project}${var.environment}storage"
  resource_group_name      = azurerm_resource_group.resource_group.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "BlobStorage"
}

resource "azurerm_service_plan" "app_service_plan" {
  name                = "${var.project}-${var.environment}-app-service-plan"
  resource_group_name = azurerm_resource_group.resource_group.name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "function_app" {
  name                = "${var.project}-${var.environment}-linux-function-app"
  resource_group_name = azurerm_resource_group.resource_group.name
  location            = var.location
  service_plan_id     = azurerm_service_plan.app_service_plan.id
  app_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.application_insights.instrumentation_key,
    "TESTSECRET"                     = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.testsecret.versionless_id})",
    "AESOAPI"                        = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.aesoapi.versionless_id})",
  }
  site_config {
    application_stack {
      python_version = "3.8"
    }
  }
  storage_account_name       = azurerm_storage_account.storage_account.name
  storage_account_access_key = azurerm_storage_account.storage_account.primary_access_key

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_key_vault" "key_vault" {
  name                = "${var.project}${var.environment}keyvault"
  resource_group_name = azurerm_resource_group.resource_group.name
  location            = var.location
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
  access_policy {

    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id


    secret_permissions = [
      "Backup",
      "Delete",
      "Get",
      "List",
      "Purge",
      "Recover",
      "Restore",
      "Set",
    ]
  }

}


resource "azurerm_key_vault_secret" "testsecret" {
  name         = "testsecret"
  value        = var.testsecret
  key_vault_id = azurerm_key_vault.key_vault.id
}
resource "azurerm_key_vault_secret" "aesoapi" {
  name         = "aesoapi"
  value        = var.aesoapi
  key_vault_id = azurerm_key_vault.key_vault.id
}

resource "azurerm_key_vault_access_policy" "key_vault_access_policy" {
  key_vault_id       = azurerm_key_vault.key_vault.id
  tenant_id          = data.azurerm_client_config.current.tenant_id
  object_id          = azurerm_linux_function_app.function_app.identity[0].principal_id
  secret_permissions = ["Get"]
}

locals {
  func_app_name      = yamldecode(file("../electricfunc/config.yaml"))["name"]
  func_app_version   = yamldecode(file("../electricfunc/config.yaml"))["version"]
  func_app_functions = yamldecode(file("../electricfunc/config.yaml"))["functions"]
}

resource "null_resource" "functions" {

  triggers = {
    functions = "${local.func_app_version}_${join("+", [for value in local.func_app_functions : value["name"]])}"
  }
  # Seems we have to wait a bit after the function app is created before the publish command will work
  provisioner "local-exec" {
    command = "sleep 30; cd ../electricfunc; func azure functionapp publish ${azurerm_linux_function_app.function_app.name}; cd ../terraform"
  }
}


data "azurerm_storage_account" "sqlstorage" {
  name                = "elctrcd${var.environment}storage"
  resource_group_name = "elctrcd-${var.environment}-resource-group"
}

resource "azurerm_container_group" "container_group" {
  name                = "${var.project}-${var.environment}-container-group"
  resource_group_name = azurerm_resource_group.resource_group.name
  location            = var.location
  ip_address_type     = "Public"
  os_type             = "Linux"

  container {
    name   = "mssql"
    image  = "mcr.microsoft.com/mssql/server:2019-latest"
    cpu    = "0.5"
    memory = "2.5"

    ports {
      port     = 1433
      protocol = "TCP"
    }

    environment_variables = {
      ACCEPT_EULA = "Y"
    }
    secure_environment_variables = {
      SA_PASSWORD = var.mssqlpass
    }

    volume {
      name                 = "alldata"
      mount_path           = "/var/opt/mssql"
      read_only            = false
      share_name           = "elctrcd${var.environment}mssql"
      storage_account_name = data.azurerm_storage_account.sqlstorage.name
      storage_account_key  = data.azurerm_storage_account.sqlstorage.primary_access_key
    }
  }
}
