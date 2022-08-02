variable "app_name" {
  description = "App name"
  default     = "european-exchange-api"
}

variable "app_name_staging" {
  description = "Staging app name"
  default = "european-exchange-api-staging"
}

variable "db_username" {
  type        = string
  description = "Database Username for Exchange Api Server"
  sensitive   = true
}

variable "db_password" {
  type        = string
  description = "Database Password for Exchange Api Server"
  sensitive   = true
}

variable "db_name" {
  type        = string
  description = "Database name"
  sensitive   = true
}

variable "stacks" {
  type        = map(string)
  description = "Available stacks"
  default     = {
    "PROD" : "PROD"
  }
}