resource "aws_iam_user" "iam_user" {
  name = var.iam_user_name
}

resource "aws_iam_user_policy" "iam_user_policy" {
  name = "AppUserRolePolicy"
  user = aws_iam_user.iam_user.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = var.allowed_user_actions
        Resource = var.allowed_user_resources
      }
    ]
  })
}