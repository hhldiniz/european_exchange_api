variable "parameter_name" {
  type = string
  description = "The name of the parameter."
}

variable "parameter_value" {
  type = string
  description = "The value of the parameter."
}

variable "parameter_type" {
  type = string
  description = "The type of the parameter."
  default = "String"
}