locals {
  database_create_script = "./create_database.sh"
}

resource "mongodbatlas_project" "atlas_project" {
  name   = "Exchange Api"
  org_id = var.mongo_organization_id
}

resource "mongodbatlas_database_user" "mongo_user" {
  project_id         = mongodbatlas_project.atlas_project.id
  username           = "backend"
  password           = var.mongo_db_password
  auth_database_name = "admin"

  roles {
    database_name = var.app_name
    role_name     = "readWrite"
  }
}

resource "mongodbatlas_cluster" "api_database_cluster" {
  cluster_type                = "REPLICASET"
  name                        = var.api_db_cluster_name
  project_id                  = mongodbatlas_project.atlas_project.id
  provider_name               = "TENANT"
  backing_provider_name       = "GCP"
  provider_region_name        = var.mongo_cluster_region
  provider_instance_size_name = "M0"
}