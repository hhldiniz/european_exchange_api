variable "example_app_name" {
  description = "App name"
  default = "exchange-api"
}

terraform {
  required_providers {
    heroku = {
      source  = "heroku/heroku"
      version = "~> 5.0"
    }
  }
}

resource "heroku_app" "european-exchange-api" {
  name   = var.example_app_name
  region = "us"
}
