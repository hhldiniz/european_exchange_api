locals {
  project_dependencies_folder = "./project_dependencies"
  get_currencies_lambda_source_path = "./${local.project_dependencies_folder}/get_currencies.zip"
  common_lambda_layer_source_path = "./${local.project_dependencies_folder}/common_layer.zip"
}

module "lambda_iam_role" {
  source = "./modules/aws/iam"
  role_name = "default-lambda-role"
}

module "lambda_get_currencies" {
  source = "./modules/aws/lambda"
  lambda_function_filename = local.get_currencies_lambda_source_path
  lambda_function_handler = "currency.get_currencies_lambda_handler"
  lambda_function_name = "${var.app_name}-get_currencies"
  lambda_function_runtime_type = "python3.10"
  lambda_iam_role_arn = module.lambda_iam_role.iam_role_arn
  layers = [module.common_layer.layer_arn]
  depends_on = [data.archive_file.zip_lambda_get_currencies, module.common_layer]
}

module "common_layer" {
  source = "./modules/aws/lambda_layer"
  lambda_layer_filename = local.common_lambda_layer_source_path
  lambda_layer_name = "CommonLayer"
  depends_on = [data.archive_file.zip_common_lambda_layer]
}

data "archive_file" "zip_lambda_get_currencies" {
  output_path = local.get_currencies_lambda_source_path
  type        = "zip"
  source_dir = "${local.project_dependencies_folder}/currency"
}

data "archive_file" "zip_common_lambda_layer" {
  output_path = local.common_lambda_layer_source_path
  type = "zip"
  source_dir = "${local.project_dependencies_folder}/common"
}