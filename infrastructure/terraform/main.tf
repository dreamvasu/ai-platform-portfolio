terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Backend configuration for state storage
  # backend "gcs" {
  #   bucket = "your-terraform-state-bucket"
  #   prefix = "terraform/state"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required GCP APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "aiplatform.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudresourcemanager.googleapis.com",
  ])

  service            = each.key
  disable_on_destroy = false
}

# Service Account for Cloud Run
resource "google_service_account" "portfolio_backend" {
  account_id   = "portfolio-backend-sa"
  display_name = "Portfolio Backend Service Account"
  description  = "Service account for portfolio backend Cloud Run service"
}

# Grant Vertex AI User role to service account
resource "google_project_iam_member" "vertex_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.portfolio_backend.email}"
}

# Grant Cloud Run Invoker role (for internal services)
resource "google_cloud_run_service_iam_member" "backend_invoker" {
  service  = google_cloud_run_service.backend.name
  location = google_cloud_run_service.backend.location
  role     = "roles/run.invoker"
  member   = "allUsers"  # Change to specific users/services in production
}

# Cloud Run Service - Backend API
resource "google_cloud_run_service" "backend" {
  name     = "portfolio-backend"
  location = var.region

  template {
    spec {
      service_account_name = google_service_account.portfolio_backend.email

      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/portfolio/backend:latest"

        ports {
          container_port = 8000
        }

        resources {
          limits = {
            memory = "2Gi"
            cpu    = "2"
          }
        }

        env {
          name  = "DJANGO_SETTINGS_MODULE"
          value = "core.settings"
        }

        env {
          name  = "GOOGLE_CLOUD_PROJECT"
          value = var.project_id
        }

        env {
          name  = "CORS_ALLOWED_ORIGINS"
          value = var.frontend_url
        }

        # Add other environment variables from Secret Manager
        # env {
        #   name = "DATABASE_URL"
        #   value_from {
        #     secret_key_ref {
        #       name = google_secret_manager_secret.database_url.secret_id
        #       key  = "latest"
        #     }
        #   }
        # }
      }

      # Minimum instances for faster cold starts
      container_concurrency = 80
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale"         = "1"
        "autoscaling.knative.dev/maxScale"         = "10"
        "run.googleapis.com/execution-environment" = "gen2"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_project_service.apis
  ]
}

# Artifact Registry Repository for Docker images
resource "google_artifact_registry_repository" "portfolio" {
  location      = var.region
  repository_id = "portfolio"
  description   = "Docker repository for portfolio application images"
  format        = "DOCKER"

  depends_on = [
    google_project_service.apis
  ]
}

# Outputs
output "backend_url" {
  value       = google_cloud_run_service.backend.status[0].url
  description = "URL of the backend Cloud Run service"
}

output "service_account_email" {
  value       = google_service_account.portfolio_backend.email
  description = "Email of the service account used by Cloud Run"
}

output "artifact_registry_url" {
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.portfolio.repository_id}"
  description = "URL for pushing Docker images"
}
