resource "aws_sns_topic_subscription" "sns_subscription" {
  endpoint  = var.endpoint
  protocol  = var.protocol
  topic_arn = var.topic_arn
}

resource "aws_lambda_permission" "with_sns" {
  count = var.protocol == "lambda" ? 1 : 0

  statement_id  = "Allow${title(var.function_name)}ExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = var.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = var.topic_arn
}