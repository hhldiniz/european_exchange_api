variable "resource_group_name_prefix" {
  default     = "rg"
  description = "Prefix of the resource group name that's combined with a random ID so name is unique in your Azure subscription."
}

variable "resource_group_location" {
  default     = "eastus"
  description = "Location of the resource group."
}

variable "subscription_id" {
  type = string
  sensitive = true
}

variable "client_id" {
  type = string
  sensitive = true
}

variable "client_secret" {
  type = string
  sensitive = true
}

variable "tenant_id" {
  type = string
  sensitive = true
}

variable "app_name" {
  type = string
  default = "european-exchange-api"
}

variable "mongoodbatlas_public_key" {
  type = string
  sensitive = true
}

variable "mongodbatlas_private_key" {
  type = string
  sensitive = true
}