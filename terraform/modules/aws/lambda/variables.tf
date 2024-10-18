variable "lambda_function_name" {
  type = string
}

variable "lambda_function_filename" {
  type = string
}

variable "lambda_function_handler" {
  type = string
}

variable "lambda_function_runtime_type" {
  type = string
}

variable "lambda_iam_role_arn" {
  type = string
}

variable "layers" {
  type = list(string)
}