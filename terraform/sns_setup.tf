module "sns_trigger_get_currencies_lambda" {
  source         = "./modules/aws/sns"
  sns_topic_name = "${var.app_name}-get-currencies-lambda-trigger"
}

module "sns_result_get_currencies_lambda" {
  source = "./modules/aws/sns"
  sns_topic_name = "${var.app_name}-get-currencies-lambda-result"
}

module "sns_trigger_get_currency_history_lambda" {
  source         = "./modules/aws/sns"
  sns_topic_name = "${var.app_name}-get-currency-history-lambda-trigger"
}

module "sns_result_get_currency_history_lambda" {
  source = "./modules/aws/sns"
  sns_topic_name = "${var.app_name}-get-currency-history-lambda-result"
}

module "sns_topic_subscription_for_get_currencies_lambda" {
  source    = "./modules/aws/sns/sns_topic_subscription"
  protocol  = "lambda"
  endpoint  = module.lambda_get_currencies.lambda_arn
  topic_arn = module.sns_trigger_get_currencies_lambda.sns_topic_arn
  function_name = module.lambda_get_currencies.function_name
  depends_on = [module.sns_trigger_get_currencies_lambda]
}

module "sns_topic_subscription_for_get_currency_history_lambda" {
  source = "./modules/aws/sns/sns_topic_subscription"
  endpoint = module.lambda_get_currency_history.lambda_arn
  protocol = "lambda"
  topic_arn = module.sns_trigger_get_currency_history_lambda.sns_topic_arn
  function_name = module.lambda_get_currency_history.function_name
  depends_on = [module.sns_trigger_get_currency_history_lambda]
}