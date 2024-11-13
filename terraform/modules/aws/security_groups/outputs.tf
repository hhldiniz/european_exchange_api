output "security_group_id" {
  value = aws_security_group.lambda_sg.id
}

output "security_group_ids" {
  value = aws_security_group.lambda_sg[*].id
}