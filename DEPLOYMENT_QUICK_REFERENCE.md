# 🚀 Quick Deployment Reference

**Status:** ✅ LIVE
**Backend:** https://portfolio-backend-eituuhu2yq-uc.a.run.app/api/
**Database:** PostgreSQL (Cloud SQL) ✅ Populated
**RAG System:** ChromaDB + Vertex AI ✅ 94 docs ingested

---

## 🔥 Quick Actions

### Test Everything
```bash
# Test API
curl https://portfolio-backend-eituuhu2yq-uc.a.run.app/api/projects/

# Test Chatbot
curl -X POST https://portfolio-backend-eituuhu2yq-uc.a.run.app/api/chatbot/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Vasus experience with GCP?", "k": 5}'
```

### Redeploy Backend
```bash
cd backend
gcloud run deploy portfolio-backend --source . --region us-central1 --env-vars-file=env.yaml --project ai-portfolio-1762033947
```

### Update Database
```bash
cd backend
DATABASE_URL="postgresql://django:OnmapREgkzsnD8vgGvZu72gwfwdjMjlk@34.31.185.136:5432/portfolio" \
venv/bin/python manage.py populate_production_data
```

### Regenerate RAG Embeddings
```bash
cd backend
GOOGLE_CLOUD_PROJECT=ai-portfolio-1762033947 \
GOOGLE_APPLICATION_CREDENTIALS=~/portfolio-gcp-key.json \
venv/bin/python ingest_documents.py

# Then redeploy to push chroma_db/
gcloud run deploy portfolio-backend --source . --region us-central1 --env-vars-file=env.yaml --project ai-portfolio-1762033947
```

---

## 🔑 Key Info

**GCP Project:** ai-portfolio-1762033947
**Region:** us-central1
**Database IP:** 34.31.185.136:5432
**DB User/Pass:** django / OnmapREgkzsnD8vgGvZu72gwfwdjMjlk
**Service Account Key:** ~/portfolio-gcp-key.json

---

## 📂 Important Files

- `backend/env.yaml` - Cloud Run environment variables
- `backend/.gcloudignore` - Deployment exclusions (⚠️ chroma_db/ should NOT be excluded)
- `backend/DEPLOYMENT_STATUS.md` - Full deployment guide
- `backend/ingest_documents.py` - RAG document ingestion
- `backend/portfolio/management/commands/populate_production_data.py` - DB population

---

## 🐛 Common Issues

**Problem:** Chatbot says "I don't have enough information"
**Fix:** Regenerate embeddings and redeploy (see above)

**Problem:** API returns 400 Bad Request
**Fix:** Check ALLOWED_HOSTS in `backend/env.yaml` includes Cloud Run URL

**Problem:** Can't connect to database locally
**Fix:** Authorize your IP:
```bash
gcloud sql instances patch portfolio-db --authorized-networks=$(curl -4 -s ifconfig.me)/32 --project ai-portfolio-1762033947
```

---

**Full Documentation:** See `backend/DEPLOYMENT_STATUS.md`
