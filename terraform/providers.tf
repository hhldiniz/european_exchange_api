terraform {
  required_version = "~>1.9.0"

  required_providers {
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "~>1.21.4"
    }
    aws = {
      source = "hashicorp/aws"
      version = "5.72.0"
    }
  }

  cloud {
    organization = "hugodiniz"
    workspaces {
      name = "european-exchange-api"
    }
  }
}

provider "aws" {
  region = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

provider "mongodbatlas" {
  public_key  = var.mongodbatlas_public_key
  private_key = var.mongodbatlas_private_key
}