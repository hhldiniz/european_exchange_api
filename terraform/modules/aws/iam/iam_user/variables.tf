variable "iam_user_name" {
  type = string
  description = "IAM user name"
}

variable "allowed_user_actions" {
  type = list(string)
  description = "Allowed actions for IAM user"
}

variable "allowed_user_resources" {
  type = list(string)
  description = "Allowed resources for IAM user"
}