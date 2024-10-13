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

variable "render_api_key" {
  type = string
  sensitive = true
}

variable "render_owner_id" {
  type = string
  sensitive = true
}