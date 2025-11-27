# iac/aws/insecure_iam_policy/main.tf
# Cria uma policy IAM extremamente permissiva e anexa a um user (intencionalmente inseguro).
# NÃO USAR EM PRODUÇÃO.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  default = "us-east-1"
}

resource "aws_iam_user" "danger_user" {
  name = "danger-user"
}

resource "aws_iam_policy" "wildcard_policy" {
  name        = "wildcard-policy-example"
  description = "Policy with * actions and * resources (insecure)"
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
POLICY
}

resource "aws_iam_policy_attachment" "attach" {
  name       = "attach-wildcard"
  users      = [aws_iam_user.danger_user.name]
  policy_arn = aws_iam_policy.wildcard_policy.arn
}
