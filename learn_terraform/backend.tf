# The block below configures Terraform to use the 'remote' backend with Terraform Cloud.
# For more information, see https://www.terraform.io/docs/backends/types/remote.html
terraform {
  # cloud {
  #   organization = "ianpreston"

  #   workspaces {
  #     name = "scratch-learn-terraform"
  #   }
  # }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }
  required_version = ">= 1.1.2"
}
