terraform {
  required_version = ">=0.12"

  required_providers {
    render = {
      source  = "render-oss/render"
      version = "1.3.0"
    }
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "~>1.4.0"
    }
  }

  cloud {
    organization = "hugodiniz"
    workspaces {
      name = "european-exchange-api"
    }
  }
}

provider "render" {
  api_key = var.render_api_key
  owner_id = var.render_owner_id
  wait_for_deploy_completion = true
}

provider "mongodbatlas" {
  public_key  = var.mongodbatlas_public_key
  private_key = var.mongodbatlas_private_key
}
