# Deployment Lessons Learned

**Last Updated:** 2025-11-03

## Critical Production Issues & Fixes

### 1. Backend Cloud Run Deployment - Port 8080 Timeout

**Error:**
```
The user-provided container failed to start and listen on the port defined by PORT=8080
```

**Root Cause:** Database connection timeout using public IP instead of Unix socket

**Fix:**
```bash
# ❌ WRONG - Public IP
DATABASE_URL=postgresql://django:password@34.31.185.136:5432/portfolio

# ✅ CORRECT - Unix Socket
DATABASE_URL=postgresql://django:password@/portfolio?host=/cloudsql/ai-portfolio-1762033947:us-central1:portfolio-db
```

**Deployment Command:**
```bash
gcloud run deploy portfolio-backend \
  --source . \
  --region=us-central1 \
  --add-cloudsql-instances=ai-portfolio-1762033947:us-central1:portfolio-db \
  --update-env-vars="DATABASE_URL=postgresql://django:OnmapREgkzsnD8vgGvZu72gwfwdjMjlk@/portfolio?host=/cloudsql/ai-portfolio-1762033947:us-central1:portfolio-db,GOOGLE_CLOUD_PROJECT=ai-portfolio-1762033947" \
  --set-secrets="SECRET_KEY=DJANGO_SECRET_KEY:latest"
```

---

### 2. Frontend Runtime Error - Undefined Array Access

**Error:**
```javascript
Uncaught TypeError: Cannot read properties of undefined (reading 'length')
```

**Root Causes:**
1. `paper.tags` was array in some cases, undefined in others
2. `project.tech_stack` could be undefined
3. `paper.abstract` was missing from API response

**Fixes:**

**Frontend - Always check arrays exist:**
```javascript
// ❌ WRONG
{paper.tags.map((tag) => ...)}
{project.tech_stack.map((tech) => ...)}

// ✅ CORRECT
{paper.tags && Array.isArray(paper.tags) && paper.tags.length > 0 && (
  paper.tags.map((tag) => ...)
)}

{project.tech_stack && Array.isArray(project.tech_stack) && project.tech_stack.length > 0 && (
  project.tech_stack.map((tech) => ...)
)}

// For optional fields
{paper.abstract && (
  <p>{paper.abstract}</p>
)}
```

**Backend - Include all fields in serializer:**
```python
# File: backend/portfolio/serializers.py

class PaperListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = [
            'id', 'title', 'abstract',  # ← Must include abstract!
            'authors', 'source', 'source_display',
            'url', 'pdf_url', 'published_date',
            'category', 'category_display',
            'citation_count', 'relevance_score',
            'is_featured', 'tags'
        ]
```

---

### 3. PostCSS/Tailwind Configuration Error

**Error:**
```
[postcss] It looks like you're trying to use `tailwindcss` directly as a PostCSS plugin
```

**Root Cause:** Mixed ES6 and CommonJS module formats

**Fix:**
```javascript
// File: frontend/tailwind.config.js
// ❌ WRONG - ES6 export
export default { ... }

// ✅ CORRECT - CommonJS
module.exports = { ... }
```

**Always use:**
- `tailwind.config.js` → `module.exports`
- `postcss.config.js` → `export default` (ES6 is OK here)

---

### 4. Paper Scraper Production Integration

**Issue:** Scraper couldn't send papers to Django in production (localhost hardcoded)

**Fix:**
```python
# File: backend/services/scraper/app/config.py

from pydantic import Field  # ← Must import Field!

class Settings(BaseSettings):
    django_api_url: str = Field(
        default="http://localhost:8000",
        description="Django API base URL"
    )
```

**Deployment:**
```bash
gcloud run deploy paper-scraper \
  --source . \
  --region=us-central1 \
  --allow-unauthenticated \
  --platform=managed \
  --memory=512Mi \
  --set-env-vars="DJANGO_API_URL=https://portfolio-backend-434831039257.us-central1.run.app,WEBHOOK_SECRET=dev-secret-change-in-production"
```

---

## Deployment Checklist

### Backend Deployment
- [ ] Use Unix socket for Cloud SQL: `host=/cloudsql/PROJECT:REGION:INSTANCE`
- [ ] Include all Cloud SQL instances: `--add-cloudsql-instances`
- [ ] Set environment variables: `DATABASE_URL`, `GOOGLE_CLOUD_PROJECT`
- [ ] Use Secret Manager for sensitive data: `--set-secrets="SECRET_KEY=..."`
- [ ] Verify Procfile uses `$PORT` variable
- [ ] Test API endpoints after deployment

### Frontend Deployment
- [ ] Check all array accesses have `Array.isArray()` guards
- [ ] Add null checks for optional fields
- [ ] Use correct module format in `tailwind.config.js` (CommonJS)
- [ ] Set production API URL in `.env.production`
- [ ] Push to GitHub (Vercel auto-deploys)
- [ ] Verify build succeeds without errors

### Microservices Integration
- [ ] Update service URLs for production (no localhost!)
- [ ] Use environment variables for external service URLs
- [ ] Test webhook integration between services
- [ ] Verify API responses match frontend expectations

---

## Production URLs

**Backend API:**
```
https://portfolio-backend-434831039257.us-central1.run.app/api/
```

**Paper Scraper:**
```
https://paper-scraper-434831039257.us-central1.run.app
```

**Frontend:**
```
https://www.vasukapoor.com
```

**Database:**
```
Cloud SQL Instance: ai-portfolio-1762033947:us-central1:portfolio-db
Connection: Unix socket at /cloudsql/ai-portfolio-1762033947:us-central1:portfolio-db
```

---

## Testing Commands

**Test Backend Health:**
```bash
curl https://portfolio-backend-434831039257.us-central1.run.app/api/
```

**Test Papers API:**
```bash
curl https://portfolio-backend-434831039257.us-central1.run.app/api/papers/ | jq '.results[0]'
```

**Trigger Paper Scraping:**
```bash
curl -X POST https://paper-scraper-434831039257.us-central1.run.app/scrape \
  -H "Content-Type: application/json" \
  -d '{"source": "arxiv", "search_terms": ["mlops"], "max_results": 10}'
```

**Check Cloud Run Logs:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=portfolio-backend" --limit 50 --format json
```

---

## Git Commits Reference

**Latest Successful Deployments:**
- Frontend fixes: `fcee026` - Fix Papers page with abstract field
- Backend serializer: `fcee026` - Add abstract to PaperListSerializer
- Scraper config: `5405366` - Configure Paper Scraper for production
- Runtime errors: `995931b` - Fix undefined array access errors
- PostCSS fix: Restored from commit `94a7222`

---

## Common Pitfalls

1. **Never hardcode localhost** in production services
2. **Always use Cloud SQL Unix sockets** in Cloud Run
3. **Check array existence** before `.map()` in React
4. **Include all fields** in Django serializers that frontend expects
5. **Use environment variables** for all service URLs
6. **Test production API responses** match frontend expectations
7. **Keep Tailwind config as CommonJS** (`module.exports`)

---

**Status:** All services deployed and working ✅
**Last Deployment:** 2025-11-03 05:50 UTC
