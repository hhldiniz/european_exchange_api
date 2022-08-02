terraform {
  required_providers {
    heroku = {
      source  = "heroku/heroku"
      version = "~> 5.0"
    }
  }
}

resource "heroku_app" "european-exchange-api" {
  buildpacks            = ["heroku/python"]
  config_vars           = {}
  internal_routing      = false
  name                  = var.app_name
  region                = "us"
  stack                 = "heroku-22"
  sensitive_config_vars = {
    "DB_NAME" : var.db_name, "DB_USER" : var.db_username, "DB_PASSWORD" : var.db_password,
    "ENVIRONMENT" : var.stacks["PROD"]
  }
}

resource "heroku_app" "european-exchange-api-staging" {
  buildpacks            = ["heroku/python"]
  config_vars           = {}
  internal_routing      = false
  name                  = var.app_name_staging
  region                = "us"
  stack                 = "heroku-22"
  sensitive_config_vars = {
    "DB_NAME" : var.db_name, "DB_USER" : var.db_username, "DB_PASSWORD" : var.db_password,
    "ENVIRONMENT" : var.stacks["PROD"]
  }
}
