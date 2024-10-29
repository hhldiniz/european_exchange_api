resource "aws_sns_topic_subscription" "sns_subscription" {
  endpoint  = var.endpoint
  protocol  = var.protocol
  topic_arn = var.topic_arn
}