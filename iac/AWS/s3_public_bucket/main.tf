# iac/aws/s3_public_bucket/main.tf
# Terraform minimal que cria um S3 público (intencionalmente inseguro).
# NÃO USAR EM PRODUÇÃO.

terraform {
  required_version = ">= 1.0"
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
  type    = string
  default = "us-east-1"
}

resource "aws_s3_bucket" "public_bucket" {
  bucket = "security-lab-public-bucket-example"
  acl    = "public-read" # vulnerabilidade: permite leitura pública
  tags = {
    Name = "security-lab-public-bucket"
  }
}

# Bloquear policies públicas é recomendado; aqui está intencionalmente aberto.
