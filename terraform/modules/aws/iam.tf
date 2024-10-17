data "aws_iam_policy_document" "aws_trust_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    effect = "Allow"
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type = "Service"
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  assume_role_policy = data.aws_iam_policy_document.aws_trust_policy.json
  name = "default-lambda_role"
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}