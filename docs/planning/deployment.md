# Deployment Guide

## Backend Deployment to GCP

### Dockerfile

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 core.wsgi:application
```

### Deploy to Cloud Run

```bash
gcloud run deploy portfolio-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="DJANGO_SETTINGS_MODULE=core.settings" \
  --memory=2Gi \
  --cpu=2
```

## Frontend Deployment to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

## Infrastructure as Code (Terraform)

### Main Configuration

```hcl
# infrastructure/terraform/main.tf

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Cloud Run Service - Backend
resource "google_cloud_run_service" "backend" {
  name     = "portfolio-backend"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/portfolio-backend:latest"

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
          name = "DATABASE_URL"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.db_url.secret_id
              key  = "latest"
            }
          }
        }
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "10"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Cloud Run Service - RAG
resource "google_cloud_run_service" "rag_service" {
  name     = "portfolio-rag"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/portfolio-rag:latest"

        resources {
          limits = {
            memory = "4Gi"
            cpu    = "2"
          }
        }
      }
    }
  }
}

# Cloud SQL Instance
resource "google_sql_database_instance" "postgres" {
  name             = "portfolio-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"
  }
}

# Allow public access
resource "google_cloud_run_service_iam_member" "backend_public" {
  service  = google_cloud_run_service.backend.name
  location = google_cloud_run_service.backend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
```

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml

name: Deploy to GCP

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - id: 'auth'
        uses: 'google-github-actions/auth@v1'
        with:
          credentials_json: '${{ secrets.GCP_SA_KEY }}'

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy portfolio-backend \
            --source ./backend \
            --region us-central1 \
            --allow-unauthenticated

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

## Performance Optimization

### SEO & Meta Tags

```jsx
// frontend/src/components/SEO.jsx

import { Helmet } from 'react-helmet-async';

export default function SEO({ title, description, image, url }) {
  return (
    <Helmet>
      <title>{title} | Vasu Kapoor - AI/ML Platform Engineer</title>
      <meta name="description" content={description} />

      {/* Open Graph */}
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image} />
      <meta property="og:url" content={url} />

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image} />
    </Helmet>
  );
}
```

### Optimization Checklist

- Image optimization
- Code splitting
- Lazy loading
- Caching strategies
- Lighthouse audit
- Google Analytics setup
- Error tracking (Sentry)
- Performance monitoring
- User behavior tracking
