locals {
  project_dependencies_folder = "./project_dependencies"
  get_currencies_lambda_source_path = "./${local.project_dependencies_folder}/currency/get_currencies.zip"
}

module "lambda_get_currencies" {
  source = "./modules/aws"
  lambda_function_filename = local.get_currencies_lambda_source_path
  lambda_function_handler = "get_currencies"
  lambda_function_name = "${var.app_name}-get_currencies"
  lambda_function_runtime_type = "python3.10"
  depends_on = [data.archive_file.zip_lambda_get_currencies]
}

data "archive_file" "zip_lambda_get_currencies" {
  output_path = local.get_currencies_lambda_source_path
  type        = "zip"
  source_dir = "${local.project_dependencies_folder}/currency"
}