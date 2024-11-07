resource "aws_ssm_parameter" "parameter" {
  name = var.parameter_name
  value = var.parameter_value
  type = var.parameter_type
}