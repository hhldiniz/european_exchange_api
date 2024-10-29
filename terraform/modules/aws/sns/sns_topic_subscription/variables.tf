variable "endpoint" {
  type = string
  description = "An ARN of a AWS resource"
}

variable "protocol" {
  type = string
  description = "The type of the SNS subscription"
}

variable "topic_arn" {
  type = string
  description = "ARN of the SNS topic to subscribe"
}