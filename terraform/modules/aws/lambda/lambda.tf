resource "aws_lambda_function" "function" {
  function_name = var.lambda_function_name
  role          = var.lambda_iam_role_arn
  filename      = var.lambda_function_filename
  handler       = var.lambda_function_handler
  runtime       = var.lambda_function_runtime_type
  timeout = var.lambda_timeout
  layers        = var.layers
  environment {
    variables = var.environment
  }
  source_code_hash = filebase64sha256(var.lambda_function_filename)
}

resource "aws_lambda_function_event_invoke_config" "lambda_event_invoke_config" {
  count = var.enable_result_publishing ? 1 : 0

  function_name = aws_lambda_function.function.function_name

  destination_config {
    on_success {
      destination = var.result_destination_arn
    }

    on_failure {
      destination = var.result_destination_arn
    }
  }
}