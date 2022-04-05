terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      # Root module should specify the maximum provider version
      # The ~> operator is a convenient shorthand for allowing only patch releases within a specific minor release.
      version = "~> 2.26"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "resource_group" {
  name     = "${var.project}-${var.environment}-resource-group"
  location = var.location
}


resource "azurerm_storage_account" "storage_account" {
  name                     = "${var.project}${var.environment}storage"
  resource_group_name      = azurerm_resource_group.resource_group.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_application_insights" "application_insights" {
  name                = "${var.project}-${var.environment}-application-insights"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name
  application_type    = "Node.JS"
}

resource "azurerm_app_service_plan" "app_service_plan" {
  name                = "${var.project}-${var.environment}-app-service-plan"
  resource_group_name = azurerm_resource_group.resource_group.name
  location            = var.location
  kind                = "FunctionApp"
  reserved            = true # this has to be set to true for Linux. Not related to the Premium Plan
  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

resource "azurerm_function_app" "function_app" {
  name                = "${var.project}-${var.environment}-function-app"
  resource_group_name = azurerm_resource_group.resource_group.name
  location            = var.location
  app_service_plan_id = azurerm_app_service_plan.app_service_plan.id
  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE"       = "",
    "FUNCTIONS_WORKER_RUNTIME"       = "python",
    "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.application_insights.instrumentation_key,
  }
  os_type = "linux"
  site_config {
    linux_fx_version          = "PYTHON|3.8"
    use_32_bit_worker_process = false
  }
  storage_account_name       = azurerm_storage_account.storage_account.name
  storage_account_access_key = azurerm_storage_account.storage_account.primary_access_key
  version                    = "~3"

  lifecycle {
    ignore_changes = [
      app_settings["WEBSITE_RUN_FROM_PACKAGE"],
    ]
  }
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
    command = "sleep 10; cd ../electricfunc; func azure functionapp publish ${azurerm_function_app.function_app.name}; cd ../terraform"
  }
}
