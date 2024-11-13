locals {
  lambda_private_subnet_cidr_block = "10.0.16.0/20"
  lambda_public_subnet_cidr_block  = "10.0.0.0/20"
}

resource "aws_eip" "nat_eip" {
  domain = "vpc"
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = module.vpc.vpc_id
}

resource "aws_nat_gateway" "nat_gateway" {
  subnet_id     = module.lambda_public_subnet.subnet_id
  allocation_id = aws_eip.nat_eip.id
}

resource "aws_route_table" "private" {
  vpc_id = module.vpc.vpc_id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat_gateway.id
  }
}

resource "aws_route_table" "public" {
  vpc_id = module.vpc.vpc_id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat_gateway.id
  }
}

resource "aws_route_table_association" "private" {
  count = length(module.lambda_private_subnet.subnet_ids)
  subnet_id      = module.lambda_private_subnet.subnet_ids[count.index]
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "public" {
  count = length(module.lambda_public_subnet.subnet_ids)
  subnet_id = module.lambda_public_subnet.subnet_ids[count.index]  # The subnet where NAT Gateway is placed
  route_table_id = aws_route_table.public.id
}

module "vpc" {
  source = "./modules/aws/vpc"
  availability_zones = ["${var.aws_region}a"]
}

module "lambda_private_subnet" {
  source             = "./modules/aws/subnets"
  availability_zones = "${var.aws_region}a"
  vpc_id             = module.vpc.vpc_id
  cidr_block         = local.lambda_private_subnet_cidr_block
}

module "lambda_public_subnet" {
  source             = "./modules/aws/subnets"
  availability_zones = "${var.aws_region}a"
  vpc_id             = module.vpc.vpc_id
  cidr_block         = local.lambda_public_subnet_cidr_block
}

module "lambda_security_group" {
  source      = "./modules/aws/security_groups"
  name_prefix = "lambda-sg"
  vpc_id      = module.vpc.vpc_id
}