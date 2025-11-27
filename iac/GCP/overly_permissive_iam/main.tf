# iac/gcp/overly_permissive_iam/main.tf
# Anexa role 'roles/owner' a um membro broad (intencionalmente inseguro).
# NÃO USAR EM PRODUÇÃO.

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project
}

variable "project" {
  default = "your-gcp-project"
}

resource "google_project_iam_binding" "owner_binding" {
  project = var.project
  role    = "roles/owner"  # vulnerabilidade: role owner muito poderosa
  members = [
    "group:all@your-domain.example" # exemplo de binding amplo
  ]
}
