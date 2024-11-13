module "lambda_iam_role" {
  source                        = "./modules/aws/iam"
  role_name                     = "default-lambda-role"
  iam_policy_name               = "lambda_logs_policy"
  iam_policy_for_attachment_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  trust_policy = {
    actions = ["sts:AssumeRole"]
    effect = "Allow"
    principals = {
      identifiers = ["lambda.amazonaws.com"]
      type = "Service"
    }
  }
  iam_policy = [
    {
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "sns:Publish"
      ]
      Effect   = "Allow"
      Resource = "*"
    }
  ]
}

module "lambda_get_currencies" {
  source                       = "./modules/aws/lambda"
  lambda_function_filename     = data.archive_file.zip_lambda_get_currencies.output_path
  lambda_function_handler      = "currency.get_currencies_lambda_handler"
  lambda_function_name         = "${var.app_name}-get_currencies"
  lambda_function_runtime_type = local.lambda_runtime
  lambda_iam_role_arn          = module.lambda_iam_role.iam_role_arn
  layers = [module.common_layer.layer_arn]
  result_destination_arn = module.sns_result_get_currencies_lambda.sns_topic_arn
  enable_result_publishing = true
  depends_on = [data.archive_file.zip_lambda_get_currencies, module.common_layer]
}

module "lambda_get_currency_history" {
  source                       = "./modules/aws/lambda"
  lambda_function_filename     = data.archive_file.zip_lambda_get_currency_history.output_path
  lambda_function_handler      = "history.get_history_lambda_handler"
  lambda_function_name         = "${var.app_name}-get_currency_history"
  lambda_function_runtime_type = local.lambda_runtime
  lambda_iam_role_arn          = module.lambda_iam_role.iam_role_arn
  layers = [module.common_layer.layer_arn]
  result_destination_arn = module.sns_result_get_currency_history_lambda.sns_topic_arn
  enable_result_publishing = true
  lambda_timeout = 30
  environment = {
    DB_USER = var.mongo_db_user
    DB_PASSWORD = var.mongo_db_password
    DB_NAME = var.app_name
    ENVIRONMENT = "PROD"
  }
  depends_on = [data.archive_file.zip_lambda_get_currency_history, module.common_layer]
}

resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = module.lambda_iam_role.iam_role_name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

module "common_layer" {
  source                = "./modules/aws/lambda/lambda_layer"
  lambda_layer_filename = data.archive_file.zip_common_lambda_layer.output_path
  lambda_layer_name     = "CommonLayer"
  depends_on = [data.archive_file.zip_common_lambda_layer]
}

data "archive_file" "zip_lambda_get_currencies" {
  output_path = local.get_currencies_lambda_source_path
  type        = "zip"
  source_dir  = "${local.project_dependencies_folder}/currency"
}

data "archive_file" "zip_lambda_get_currency_history" {
  output_path = local.get_currency_history_lambda_source_path
  type        = "zip"
  source_dir  = "${local.project_dependencies_folder}/history"
}

data "archive_file" "zip_common_lambda_layer" {
  output_path = local.common_lambda_layer_source_path
  type        = "zip"
  source_dir  = "${local.project_dependencies_folder}/common"
  depends_on = [null_resource.install_external_dependencies]
}

resource "null_resource" "install_external_dependencies" {
  for_each = toset(local.modules)
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
    command = "pip install -r ${local.project_dependencies_folder}/${each.value}/requirements.txt --target ${local.dependencies_instalation_folder}"
  }
}