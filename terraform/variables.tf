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

variable "aws_region" {
  type = string
  default = "sa-east-1"
}

variable "aws_access_key" {
  type = string
  sensitive = true
}

variable "aws_secret_key" {
  type = string
  sensitive = true
}

variable "master_api_key" {
  type = string
  sensitive = true
}

variable "flagsmith_project_uuid" {
  type = string
  sensitive = true
  description = "UUID of the Flagsmith project"
}