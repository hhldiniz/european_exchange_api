locals {
  project_dependencies_folder = "./project_dependencies"
  get_currencies_lambda_source_path = "./${local.project_dependencies_folder}/get_currencies.zip"
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
  depends_on = [data.archive_file.zip_lambda_get_currencies]
}

data "archive_file" "zip_lambda_get_currencies" {
  output_path = local.get_currencies_lambda_source_path
  type        = "zip"
  source_dir = "${local.project_dependencies_folder}/currency"
}