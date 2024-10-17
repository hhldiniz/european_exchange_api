resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name = var.lambda_layer_name
  filename = var.lambda_layer_filename
  compatible_runtimes = ["python3.x"]
}