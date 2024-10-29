resource "aws_sns_topic" "lambda_trigger" {
  name = var.sns_topic_name
}