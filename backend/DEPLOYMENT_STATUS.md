# 🚀 Deployment Status & Guide

**Last Updated:** November 2, 2025
**Status:** ✅ FULLY DEPLOYED & WORKING

---

## 📊 Current Deployment

### Backend (Django + RAG)
- **Platform:** GCP Cloud Run
- **URL:** https://portfolio-backend-eituuhu2yq-uc.a.run.app
- **Region:** us-central1
- **Project ID:** ai-portfolio-1762033947
- **Service Name:** portfolio-backend
- **Latest Revision:** portfolio-backend-00014-nsb (deployed Nov 2, 2025)

### Database (PostgreSQL)
- **Platform:** GCP Cloud SQL
- **Instance:** portfolio-db
- **Database:** portfolio
- **User:** django
- **Password:** OnmapREgkzsnD8vgGvZu72gwfwdjMjlk
- **IP:** 34.31.185.136:5432
- **Connection:** Cloud SQL Unix socket (`/cloudsql/ai-portfolio-1762033947:us-central1:portfolio-db`)

### Vector Store (ChromaDB)
- **Status:** ✅ Deployed with backend container
- **Location:** `/workspace/chroma_db/` (in Cloud Run)
- **Documents:** 94 chunks from 38 source files
- **Embeddings:** Google Vertex AI (`textembedding-gecko`)

---

## ✅ What's Working

1. **Django REST API**
   - ✅ `/api/tech-stack/` - 13 technologies
   - ✅ `/api/journey/` - 11 journey entries
   - ✅ `/api/projects/` - 6 projects (includes Calibra & Ringlet)

2. **RAG Chatbot**
   - ✅ `/api/chatbot/health/` - Health check
   - ✅ `/api/chatbot/query/` - Q&A endpoint
   - ✅ Answers questions about GCP, projects, tech stack, journey
   - ✅ Returns sources with relevance scores

3. **Data Populated**
   - ✅ PostgreSQL database fully populated
   - ✅ ChromaDB vector store ingested
   - ✅ All case studies (Calibra, Ringlet) included

---

## 🔑 Important Files

### Configuration
- `env.yaml` - Environment variables for Cloud Run
- `.gcloudignore` - Deployment exclusions (⚠️ chroma_db/ is NOT excluded)
- `Procfile` - Buildpack entry point
- `requirements.txt` - Python dependencies

### Database Population
- `portfolio/management/commands/populate_production_data.py` - Populates PostgreSQL
- `ingest_documents.py` - Populates ChromaDB vector store

### Key Scripts
- `add_calibra_project.py` - Adds Calibra case study
- `add_ringlet_project.py` - Adds Ringlet case study

---

## 🔄 How to Update & Redeploy

### Update Backend Code
```bash
# From backend directory
gcloud run deploy portfolio-backend \
  --source . \
  --region us-central1 \
  --env-vars-file=env.yaml \
  --project ai-portfolio-1762033947
```

### Update PostgreSQL Data
```bash
# Run locally (requires authorized IP)
DATABASE_URL="postgresql://django:OnmapREgkzsnD8vgGvZu72gwfwdjMjlk@34.31.185.136:5432/portfolio" \
venv/bin/python manage.py populate_production_data
```

### Update ChromaDB Vector Store
```bash
# Run locally to regenerate embeddings
GOOGLE_CLOUD_PROJECT=ai-portfolio-1762033947 \
GOOGLE_APPLICATION_CREDENTIALS=~/portfolio-gcp-key.json \
venv/bin/python ingest_documents.py

# Then redeploy to push chroma_db/ to Cloud Run
gcloud run deploy portfolio-backend --source . --region us-central1 --env-vars-file=env.yaml --project ai-portfolio-1762033947
```

### Update Environment Variables
```bash
# Edit env.yaml, then:
gcloud run services update portfolio-backend \
  --region us-central1 \
  --env-vars-file=env.yaml \
  --project ai-portfolio-1762033947
```

---

## 🛠️ Troubleshooting

### Issue: 400 Bad Request on API calls
**Cause:** ALLOWED_HOSTS doesn't include the Cloud Run URL
**Fix:** Update `env.yaml` with correct URL, redeploy

### Issue: "I don't have enough information" from chatbot
**Cause:** ChromaDB not deployed or empty
**Fix:**
1. Run `ingest_documents.py` locally
2. Verify `chroma_db/` is NOT in `.gcloudignore`
3. Redeploy backend

### Issue: Database connection timeout from local machine
**Cause:** Your IP not authorized
**Fix:**
```bash
# Get your IP
curl -4 ifconfig.me

# Add to Cloud SQL
gcloud sql instances patch portfolio-db \
  --authorized-networks=YOUR_IP/32 \
  --project ai-portfolio-1762033947
```

### Issue: Cloud Run job fails (populate-db)
**Cause:** Buildpacks don't expose python command
**Fix:** Use local database population instead (see above)

---

## 📦 What's Deployed

### Source Files Ingested (94 chunks)
- Planning docs (9 files): architecture, timeline, deployment, etc.
- Technical docs (1 file): RAG implementation
- Case studies (5 files): Calibra, Ringlet
- Root files (23 files): README, GCP guides, etc.

### Database Records
- **Tech Stack:** React, Django, PostgreSQL, Kubernetes, GCP, Terraform, ChromaDB, OpenAI, etc.
- **Journey:** 11 hour-by-hour entries of the 12-hour sprint
- **Projects:** 6 total (4 base + Calibra + Ringlet)

---

## 🔐 Credentials & Access

### GCP Service Account
- **Key Location:** `~/portfolio-gcp-key.json`
- **Project:** ai-portfolio-1762033947
- **Email:** (set in service account)

### Cloud SQL
- **Connection from Cloud Run:** Unix socket (no password needed)
- **Connection from local:** TCP with IP authorization required

### Vertex AI
- **Embedding Model:** textembedding-gecko
- **Dimensions:** 768
- **Auth:** Application Default Credentials

---

## 🚨 Critical Notes

1. **Don't exclude chroma_db/** - The RAG system needs this deployed
2. **ALLOWED_HOSTS must include Cloud Run URL** - Check both URLs (eituuhu2yq and 434831039257)
3. **Local IP changes** - Re-authorize if you can't connect to Cloud SQL
4. **ChromaDB is stateless on Cloud Run** - Rebuilds on each deploy unless included in deployment

---

## 📞 Quick Commands

```bash
# Check deployment status
gcloud run services describe portfolio-backend --region us-central1 --project ai-portfolio-1762033947

# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=portfolio-backend" --limit 50 --project ai-portfolio-1762033947

# Test API endpoints
curl https://portfolio-backend-eituuhu2yq-uc.a.run.app/api/projects/
curl https://portfolio-backend-eituuhu2yq-uc.a.run.app/api/chatbot/health/
curl -X POST https://portfolio-backend-eituuhu2yq-uc.a.run.app/api/chatbot/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Vasus experience with GCP?", "k": 5}'

# Check Cloud SQL
gcloud sql instances describe portfolio-db --project ai-portfolio-1762033947

# List revisions
gcloud run revisions list --service portfolio-backend --region us-central1 --project ai-portfolio-1762033947
```

---

## ✅ Success Checklist

- [x] Backend deployed to Cloud Run
- [x] PostgreSQL database populated
- [x] ChromaDB vector store populated and deployed
- [x] RAG chatbot answering questions correctly
- [x] All API endpoints responding
- [x] ALLOWED_HOSTS configured correctly
- [x] Environment variables set
- [x] Cloud SQL connection working
- [x] Vertex AI embeddings functional

---

**Next Steps:**
1. Deploy frontend to Vercel
2. Connect frontend to backend API
3. Test chatbot widget on frontend
4. Set up custom domain (optional)
5. Monitor costs and usage

**Estimated Monthly Cost:** ~$20-30
- Cloud Run: ~$5-10 (with generous free tier)
- Cloud SQL: ~$10-15 (db-f1-micro)
- Vertex AI: ~$5 (low usage)
