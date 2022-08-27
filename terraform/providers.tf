terraform {
  required_version = ">=0.12"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
    provider "mongodbatlas" {
    public_key = var.mongodbatlas_public_key
    private_key  = var.mongodbatlas_private_key
}
  }

  cloud {
    organization = "hugodiniz"
    workspaces {
      name = "european-exchange-api"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}
