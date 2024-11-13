variable "name_prefix" {
  type = string
  description = "prefix to use when naming resources"
}

variable "vpc_id" {
  type = string
  description = "ID of the VPC to create the security group in"
}