variable "vpc_id" {
  type = string
  description = "VPC ID"
}

variable "cidr_block" {
  type = string
  description = "CIDR block"
}

variable "availability_zones" {
  type = string
  description = "Availability zones"
}