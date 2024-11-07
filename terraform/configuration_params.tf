module "ssm_parameter_aws_region" {
  source = "./modules/aws/ssm_parameter"
  parameter_name = "configuration_aws_region"
  parameter_value = var.aws_region
}