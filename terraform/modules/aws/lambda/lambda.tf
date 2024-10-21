resource "aws_lambda_function" "function" {
  function_name = var.lambda_function_name
  role          = var.lambda_iam_role_arn
  filename = var.lambda_function_filename
  handler = var.lambda_function_handler
  runtime = var.lambda_function_runtime_type
  layers = var.layers
  source_code_hash = filebase64sha256(var.lambda_function_filename)
}