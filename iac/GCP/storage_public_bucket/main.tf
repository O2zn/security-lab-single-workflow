# iac/gcp/storage_public_bucket/main.tf
# Cria um bucket GCS público (intencionalmente inseguro).
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
  region  = var.region
}

variable "project" {
  type    = string
  default = "your-gcp-project"
}

variable "region" {
  type    = string
  default = "us-central1"
}

resource "google_storage_bucket" "public_bucket" {
  name     = "security-lab-public-bucket-example-gcp"
  location = var.region
  uniform_bucket_level_access = true
  force_destroy = true
}

# Binding that makes the bucket publicly readable
resource "google_storage_bucket_iam_member" "all_users_reader" {
  bucket = google_storage_bucket.public_bucket.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"  # vulnerabilidade: público
}
