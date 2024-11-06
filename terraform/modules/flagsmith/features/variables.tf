variable "feature_name" {
  type        = string
  description = "Name of the Flagsmith feature"
}

variable "project_uuid" {
  type        = string
  sensitive = true
  description = "UUID of the Flagsmith project"
}

variable "feature_description" {
  type = string
}

variable "feature_type" {
  type = string
  default = "STANDARD"
  description = "Type of the segment. Can be 'STANDARD' or 'MULTIVARIATE'."
}

variable "flagsmith_api_key" {
  type = string
  sensitive = true
  description = "Flagsmith API key"
}

variable "feature_state_value" {
  type = any
  default = null
  description = "Value of the feature state."
}

variable "feature_enabled" {
  type = bool
  default = true
  description = "Whether the feature is enabled or not."
}