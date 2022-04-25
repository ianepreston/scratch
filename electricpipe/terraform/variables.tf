variable "project" {
  type        = string
  description = "Project name"
}

variable "environment" {
  type        = string
  description = "Environment (dev / stage / prod)"
}

variable "location" {
  type        = string
  description = "Azure region to deploy module to"
}

variable "testsecret" {
  type        = string
  sensitive   = true
  description = "A test secret to put in Azure secret vault"
}

variable "aesoapi" {
  type        = string
  sensitive   = true
  description = "API key to access Alberta Electric System Operator data"
}

variable "mssqlpass" {
  type        = string
  sensitive   = true
  description = "Password to MS SQL server db"
}
