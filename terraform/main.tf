locals {
  resource_group_name = azurerm_resource_group.rg.name
}

resource "random_pet" "rg_name" {
  prefix = var.resource_group_name_prefix
}

resource "azurerm_resource_group" "rg" {
  name     = random_pet.rg_name.id
  location = var.resource_group_location
}

resource "azurerm_service_plan" "european_exchange_api_service_plan" {
  name                = var.app_name
  resource_group_name = local.resource_group_name
  location            = var.resource_group_location
  os_type             = "Linux"
  sku_name            = "F1"
}

resource "azurerm_linux_web_app" "european_exchange_api_web_app" {
  name                = var.app_name
  resource_group_name = local.resource_group_name
  location            = var.resource_group_location
  service_plan_id     = azurerm_service_plan.european_exchange_api_service_plan.id
  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = true
    "WEBSITE_HTTPLOGGING_RETENTION_DAYS" = var.log_retention_days
    "ENVIRONMENT" = "PRODUCTION"
    "DB_USER" = var.mongo_db_user
    "DB_PASSWORD" = var.mongo_db_password
    "DB_NAME" = var.api_db_cluster_name
  }
  logs {
    application_logs {
      file_system_level = var.log_level
    }
    http_logs {
      file_system {
        retention_in_days = var.log_retention_days
        retention_in_mb = 35
      }
    }
  }

  site_config {
    always_on        = false
    app_command_line = "gunicorn --bind 0.0.0.0 wsgi:app"

    application_stack {
      python_version = "3.9"
    }

  }
}

resource "azurerm_app_service_source_control" "sourcecontrol" {
  app_id                 = azurerm_linux_web_app.european_exchange_api_web_app.id
  repo_url               = "https://github.com/hhldiniz/european_exchange_api"
  branch                 = "master"
  use_manual_integration = false
  use_mercurial          = false
  github_action_configuration {
    generate_workflow_file = true
  }

  timeouts {}

}
