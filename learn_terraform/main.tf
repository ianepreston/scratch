# Configure the Azure provider
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "D-CC-RG-terraformtest"
  location = "canadacentral"
}
