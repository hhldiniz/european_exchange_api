locals {
  project_dependencies_folder             = "./project_dependencies"
  get_currencies_lambda_file_name         = "get_currencies.zip"
  get_currency_history_file_name          = "get_currency_history.zip"
  common_layer_file_name                  = "common_layer.zip"
  dependencies_instalation_folder         = "${local.project_dependencies_folder}/common/python"
  get_currencies_lambda_source_path       = "./${local.project_dependencies_folder}/${local.get_currencies_lambda_file_name}"
  get_currency_history_lambda_source_path = "./${local.project_dependencies_folder}/${local.get_currency_history_file_name}"
  common_lambda_layer_source_path         = "./${local.project_dependencies_folder}/${local.common_layer_file_name}"
  lambda_runtime                          = "python3.10"
  modules = ["common", "currency"]
}

module "cotacaodireta_aws_iam_user" {
  source        = "./modules/aws/iam/iam_user"
  iam_user_name = "cotacaodireta"
  allowed_user_actions = [
    "sns:Publish",
    "ssm:GetParameter",
    "ssm:GetParameters",
    "ssm:GetParametersByPath"
  ]
  allowed_user_resources = [
    "arn:aws:ssm:*:*:parameter/*"
  ]
}