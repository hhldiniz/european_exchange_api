resource "mongodbatlas_project" "atlas_project" {
  name   = "Exchange Api"
  org_id = var.mongo_organization_id
}

resource "mongodbatlas_database_user" "mongo_user" {
  project_id = mongodbatlas_project.atlas_project.id
  username   = "backend"
  roles { role_name = "readWriteAnyDatabase" }
}

resource "mongodbatlas_advanced_cluster" "api_database_cluster" {
  cluster_type = "REPLICASET"
  name         = var.api_db_cluster_name
  project_id   = mongodbatlas_project.atlas_project.id
  replication_specs {
    region_configs {
      electable_specs {
        instance_size = "M0"
      }
      priority      = 1
      provider_name = "GCP"
      region_name   = var.mongo_cluster_region
    }
  }
}