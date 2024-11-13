resource "aws_security_group" "lambda_sg" {
  name_prefix = var.name_prefix
  description = "Security group for lambda function"

  vpc_id      = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}