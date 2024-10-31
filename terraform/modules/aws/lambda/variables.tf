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

variable "result_destination_arn" {
  type        = string
  description = "An ARN that represents the destination for publishing the SNS message with the Lambda Function invocation result"
  default = null
}

variable "enable_result_publishing" {
  type = bool
  default = false
  description = "Enable or disable the result publishing to an SNS topic"
}

variable "lambda_timeout" {
  type = number
  default = 3
  description = "The amount of time your Lambda Function has to run in seconds."
}