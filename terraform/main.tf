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


  site_config {
    always_on         = false

    application_stack {
      python_version = "3.9"
    }

  }
}

resource "azurerm_app_service_source_control" "sourcecontrol" {
  app_id             = azurerm_linux_web_app.european_exchange_api_web_app.id
  repo_url           = "https://github.com/hhldiniz/european_exchange_api"
  branch             = "master"
  use_manual_integration = false
  use_mercurial      = false
}