variable "cidr_block" {
  type = string
  default = "10.0.0.0/16"
  description = "CIDR block for the VPC"
}

variable "availability_zones" {
  type = list(string)
  description = "Availability zones for the VPC"
}