variable "trust_policy" {
  type = object({
    actions = list(string)
    effect = string
    principals = object({
      identifiers = list(string)
      type = string
    })
  })
  description = "AWS trust policy statement"
}

variable "role_name" {
  type = string
}

variable "iam_policy" {
  type = list(object({
    Action = list(string)
    Effect   = string
    Resource = string
  }))
  description = "The 'Statement' portion of an IAM policy definition"
}

variable "iam_policy_name" {
  type = string
  description = "Name for the IAM policy resource"
}

variable "iam_policy_for_attachment_arn" {
  type = string
  description = "Policy ARN to attach to a IAM Role"
  default = null
}