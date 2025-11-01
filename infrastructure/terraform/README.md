# Terraform Infrastructure as Code for GCP

This directory contains Terraform configurations to provision and manage GCP infrastructure for the AI/ML portfolio.

## What This Provisions

1. **Cloud Run Service** - Serverless container for Django backend
2. **Service Account** - IAM identity with Vertex AI permissions
3. **Artifact Registry** - Docker image repository
4. **API Enablement** - Required GCP APIs (Cloud Run, Vertex AI, etc.)
5. **IAM Bindings** - Proper permissions for services

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    INTERNET                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          CLOUD RUN SERVICE (portfolio-backend)          │
│  • Serverless containers (1-10 instances)               │
│  • Auto-scaling based on requests                       │
│  • HTTPS endpoint                                       │
│  • Service Account: portfolio-backend-sa                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              VERTEX AI APIS                              │
│  • Text Embeddings (textembedding-gecko)                │
│  • Gemini Pro (generative AI)                           │
└─────────────────────────────────────────────────────────┘
```

## Prerequisites

1. **GCP Account** with billing enabled
2. **gcloud CLI** installed and authenticated
3. **Terraform** >= 1.0 installed
4. **GCP Project** created

## Setup

### 1. Initialize GCP

```bash
# Login to GCP
gcloud auth login
gcloud auth application-default login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs manually (or let Terraform do it)
gcloud services enable run.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

### 2. Configure Terraform Variables

```bash
# Copy example file
cp terraform.tfvars.example terraform.tfvars

# Edit with your values
vim terraform.tfvars
```

Example `terraform.tfvars`:
```hcl
project_id   = "my-portfolio-project"
region       = "us-central1"
frontend_url = "https://my-portfolio.vercel.app"
environment  = "prod"
```

### 3. Initialize Terraform

```bash
cd infrastructure/terraform

# Initialize providers
terraform init

# (Optional) Configure remote state in GCS
# Uncomment backend block in main.tf and run:
# terraform init -backend-config="bucket=your-state-bucket"
```

### 4. Plan Changes

```bash
# Preview what will be created
terraform plan

# Save plan to file
terraform plan -out=tfplan
```

### 5. Apply Infrastructure

```bash
# Apply changes
terraform apply

# Or apply saved plan
terraform apply tfplan
```

### 6. Build and Deploy Application

```bash
# Get Artifact Registry URL from Terraform output
terraform output artifact_registry_url

# Build and push Docker image
cd ../../backend
gcloud builds submit --tag ARTIFACT_REGISTRY_URL/backend:latest

# Update Cloud Run with new image
gcloud run deploy portfolio-backend \
  --image ARTIFACT_REGISTRY_URL/backend:latest \
  --region us-central1
```

## Terraform Commands

### View Current State
```bash
terraform show
```

### View Outputs
```bash
terraform output
terraform output backend_url
```

### Format Code
```bash
terraform fmt -recursive
```

### Validate Configuration
```bash
terraform validate
```

### Destroy Infrastructure
```bash
# WARNING: This deletes all resources
terraform destroy

# Destroy specific resource
terraform destroy -target=google_cloud_run_service.backend
```

## Outputs

After `terraform apply`, you'll see:

```
Outputs:

artifact_registry_url = "us-central1-docker.pkg.dev/my-project/portfolio"
backend_url = "https://portfolio-backend-xxxxx-uc.a.run.app"
service_account_email = "portfolio-backend-sa@my-project.iam.gserviceaccount.com"
```

## State Management

### Local State (Default)
Terraform stores state in `terraform.tfstate` file locally.

**⚠️ Warning:** Do not commit this file to git! It contains sensitive information.

### Remote State (Recommended for Teams)

1. Create GCS bucket for state:
```bash
gsutil mb gs://your-terraform-state-bucket
gsutil versioning set on gs://your-terraform-state-bucket
```

2. Uncomment backend block in `main.tf`:
```hcl
backend "gcs" {
  bucket = "your-terraform-state-bucket"
  prefix = "terraform/state"
}
```

3. Re-initialize:
```bash
terraform init -migrate-state
```

## Cost Estimates

### Cloud Run
- **Free tier:** 2 million requests/month
- **CPU:** $0.00002400 per vCPU-second
- **Memory:** $0.00000250 per GiB-second
- **Estimated cost:** $5-20/month (depends on traffic)

### Vertex AI
- **Text Embeddings:** ~$0.00002 per 1K characters
- **Gemini Pro:** ~$0.00025 per 1K characters
- **Estimated cost:** $1-5/month (100-500 queries)

### Artifact Registry
- **Storage:** $0.10 per GB per month
- **Estimated cost:** < $1/month

**Total Estimated Monthly Cost:** $10-30 for low traffic

## Production Considerations

### 1. Security
- [ ] Use Secret Manager for sensitive data
- [ ] Enable VPC Service Controls
- [ ] Implement least privilege IAM
- [ ] Use Workload Identity instead of service account keys

### 2. High Availability
- [ ] Set minScale > 0 to avoid cold starts
- [ ] Configure health checks
- [ ] Set up uptime monitoring
- [ ] Implement retry logic in application

### 3. Cost Optimization
- [ ] Review auto-scaling settings
- [ ] Set maxScale to prevent runaway costs
- [ ] Use committed use discounts
- [ ] Enable container image streaming

### 4. Monitoring
- [ ] Set up Cloud Monitoring alerts
- [ ] Configure log-based metrics
- [ ] Create custom dashboards
- [ ] Set up error reporting

### 5. CI/CD
- [ ] Integrate with Cloud Build
- [ ] Set up GitHub Actions
- [ ] Implement blue-green deployments
- [ ] Add automated testing

## Troubleshooting

### Authentication Errors
```bash
# Re-authenticate
gcloud auth application-default login

# Verify credentials
gcloud auth list
```

### Permission Denied
```bash
# Check project IAM
gcloud projects get-iam-policy YOUR_PROJECT_ID

# Grant yourself necessary roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/editor"
```

### Service Not Deploying
```bash
# Check Cloud Run logs
gcloud run services logs read portfolio-backend --region=us-central1

# Check build logs
gcloud builds list
gcloud builds log BUILD_ID
```

## Best Practices

1. **Version Control:** Commit Terraform files, exclude `.tfstate` and `.tfvars`
2. **Modules:** Break down into reusable modules for larger projects
3. **Workspaces:** Use Terraform workspaces for dev/staging/prod
4. **Documentation:** Keep README updated with any infrastructure changes
5. **Testing:** Use `terraform plan` before every apply
6. **Tagging:** Add labels to resources for cost tracking
7. **Backup:** Regularly backup Terraform state
8. **Review:** Have someone review infrastructure changes before applying

## Additional Resources

- [Terraform GCP Provider Docs](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)

## Support

For issues with:
- **Terraform:** Check [Terraform Registry](https://registry.terraform.io/)
- **GCP:** Check [Google Cloud Support](https://cloud.google.com/support)
- **This Portfolio:** Create an issue in the GitHub repository
