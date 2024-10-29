data "aws_iam_policy_document" "aws_trust_policy" {
  statement {
    actions = var.trust_policy["actions"]
    effect = var.trust_policy["effect"]
    principals {
      identifiers = var.trust_policy["principals"]["identifiers"]
      type = var.trust_policy["principals"]["type"]
    }
  }
}

resource "aws_iam_role" "role" {
  assume_role_policy = data.aws_iam_policy_document.aws_trust_policy.json
  name               = var.role_name
}

resource "aws_iam_role_policy_attachment" "policy" {
  lifecycle {
    precondition {
      condition = var.iam_policy_for_attachment_arn != null
      error_message = "var.iam_policy_for_attachment_arn must be provided!"
    }
  }
  role       = aws_iam_role.role.name
  policy_arn = var.iam_policy_for_attachment_arn
}

resource "aws_iam_role_policy_attachment" "lambda_logs_policy" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.iam_policy.arn
}

resource "aws_iam_policy" "iam_policy" {
  name = var.iam_policy_name
  path = "/"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = var.iam_policy
  })
}