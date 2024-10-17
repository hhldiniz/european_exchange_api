resource "aws_lambda_function" "function" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_role.arn
  filename = var.lambda_function_filename
  handler = var.lambda_function_handler
  runtime = var.lambda_function_runtime_type
  source_code_hash = filebase64sha256(var.lambda_function_filename)
}