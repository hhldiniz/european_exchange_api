variable "resource_group_name_prefix" {
  default     = "rg"
  description = "Prefix of the resource group name that's combined with a random ID so name is unique in your Azure subscription."
}

variable "resource_group_location" {
  default     = "brazilsouth"
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

variable "mongodbatlas_public_key" {
  type = string
  sensitive = true
}

variable "mongodbatlas_private_key" {
  type = string
  sensitive = true
}

variable "mongo_db_user" {
  type = string
  sensitive = true
}

variable "mongo_db_password" {
  type = string
  sensitive = true
}

variable "mongo_organization_id" {
  type = string
  sensitive = true
}

variable "api_db_cluster_name" {
  type = string
  default = "exhange-api-cluster"
}

variable "mongo_cluster_region" {
  type = string
  default = "SOUTH_AMERICA_EAST_1"
}