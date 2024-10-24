locals {
  project_dependencies_folder       = "./project_dependencies"
  get_currencies_lambda_file_name = "get_currencies.zip"
  get_currency_history_file_name = "get_currency_history.zip"
  common_layer_file_name = "common_layer.zip"
  dependencies_instalation_folder = "${local.project_dependencies_folder}/common/python"
  get_currencies_lambda_source_path = "./${local.project_dependencies_folder}/${local.get_currencies_lambda_file_name}"
  get_currency_history_lambda_source_path = "./${local.project_dependencies_folder}/${local.get_currency_history_file_name}"
  common_lambda_layer_source_path   = "./${local.project_dependencies_folder}/${local.common_layer_file_name}"
  lambda_runtime = "python3.10"
  modules = ["common", "currency"]
}

module "lambda_iam_role" {
  source    = "./modules/aws/iam"
  role_name = "default-lambda-role"
}

module "lambda_get_currencies" {
  source                       = "./modules/aws/lambda"
  lambda_function_filename     = data.archive_file.zip_lambda_get_currencies.output_path
  lambda_function_handler      = "currency.get_currencies_lambda_handler"
  lambda_function_name         = "${var.app_name}-get_currencies"
  lambda_function_runtime_type = local.lambda_runtime
  lambda_iam_role_arn          = module.lambda_iam_role.iam_role_arn
  layers = [module.common_layer.layer_arn]
  depends_on = [data.archive_file.zip_lambda_get_currencies, module.common_layer]
}

module "lambda_get_currency_history" {
  source = "./modules/aws/lambda"
  lambda_function_filename     = data.archive_file.zip_lambda_get_currency_history.output_path
  lambda_function_handler      = "history.get_history_lambda_handler"
  lambda_function_name         = "${var.app_name}-get_currency_history"
  lambda_function_runtime_type = local.lambda_runtime
  lambda_iam_role_arn          = module.lambda_iam_role.iam_role_arn
  layers = [module.common_layer.layer_arn]
  depends_on = [data.archive_file.zip_lambda_get_currency_history, module.common_layer]
}

module "common_layer" {
  source                = "./modules/aws/lambda_layer"
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
  source_dir = "${local.project_dependencies_folder}/history"
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