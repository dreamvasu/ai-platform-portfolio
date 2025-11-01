# AI/ML Platform Engineer Portfolio - Build Plan

**Project:** "The 12-Hour Sprint - Journey to AI Platform Engineering"
**Builder:** Vasu Kapoor
**Purpose:** Build a living portfolio proving learning velocity and technical depth
**Timeline:** 14-16 hours total
**Deploy:** GCP (Cloud Run) + Vercel

---

## 🎯 Project Vision

Build a **self-documenting portfolio** showcasing the 12-hour sprint journey from 65% match to 90%+ match for Wipro AI/ML Platform Engineer role.

**This is a proof system:**
- ✅ Proves fast learning (the sprint itself)
- ✅ Proves full-stack skills (React + Django)
- ✅ Proves AI/ML skills (RAG chatbot)
- ✅ Proves platform skills (K8s, GCP, IaC)
- ✅ Proves shipping ability (live deployment)

**The Killer Feature:** RAG-powered chatbot that answers questions about YOUR journey using YOUR documentation as the knowledge base.

---

## 📚 Detailed Documentation

All detailed planning is in `docs/planning/`:

1. **[Architecture & Structure](./docs/planning/architecture.md)**
   - System architecture diagrams
   - Tech stack breakdown (React, Django, GCP, K8s, Terraform)
   - Complete project structure

2. **[Frontend Design](./docs/planning/frontend-design.md)**
   - Home/Landing page layout
   - Journey timeline page
   - Technical deep dive pages (K8s, GCP, RAG, Terraform)
   - About page & Blog structure

3. **[Backend & RAG Implementation](./docs/planning/backend-rag.md)**
   - RAG chatbot architecture
   - Vector store setup (ChromaDB)
   - Document ingestion pipeline
   - Complete code examples

4. **[Deployment Guide](./docs/planning/deployment.md)**
   - GCP Cloud Run deployment
   - Vercel frontend deployment
   - Terraform IaC configurations
   - CI/CD with GitHub Actions

5. **[Timeline & Phases](./docs/planning/timeline-phases.md)**
   - Phase-by-phase implementation (15-19 hours)
   - Hour-by-hour breakdown
   - Quick start commands

6. **[Job Application Strategy](./docs/planning/job-application.md)**
   - Resume updates
   - LinkedIn post templates
   - Cover letter hooks
   - Interview talking points

7. **[Quick Reference](./docs/planning/quick-reference.md)**
   - Success metrics & checklists
   - Cost estimates ($20-30/month)
   - Documentation standards
   - Support resources

---

## ⚡ Quick Start (30 Minutes)

```bash
# 1. Create repo
git init ai-platform-portfolio
cd ai-platform-portfolio

# 2. Setup frontend
npm create vite@latest frontend -- --template react
cd frontend && npm install tailwindcss framer-motion react-router-dom axios react-markdown

# 3. Setup backend
mkdir backend && cd backend
python -m venv venv && source venv/bin/activate
pip install django djangorestframework django-cors-headers chromadb openai
django-admin startproject core .
python manage.py startapp portfolio
python manage.py startapp rag_service

# 4. Create infrastructure
mkdir -p infrastructure/{terraform,kubernetes}
mkdir -p docs/{journey,technical,planning,blog}

# 5. Start building!
code .
```

---

## 📊 Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| Foundation | 4-5h | Basic app, API, local dev setup |
| Content | 4-5h | Documentation, pages, visuals |
| RAG Chatbot | 3-4h | Vector store, query system, widget |
| Deployment | 2-3h | GCP, Vercel, IaC, CI/CD |
| Polish | 2h | Performance, SEO, testing |
| **TOTAL** | **15-19h** | **Production-ready portfolio** |

See [timeline-phases.md](./docs/planning/timeline-phases.md) for detailed breakdown.

---

## 🎯 Success Criteria

### Technical
- ✅ Frontend deployed and accessible
- ✅ Backend API responding < 200ms
- ✅ RAG chatbot accuracy > 85%
- ✅ Lighthouse score > 90

### Content
- ✅ Complete journey documentation
- ✅ 4+ technical deep dives
- ✅ 50+ GitHub commits
- ✅ Live deployment proof

### Impact
- ✅ Job application submitted
- ✅ Portfolio URL in resume
- ✅ LinkedIn post published

---

## 🚀 The Reality Check

**Without this portfolio:**
- "Another candidate" with 15% interview chance
- Weak position: "I can learn it"

**With this portfolio:**
- "Fast learner with receipts" with 70% interview chance
- Strong position: "I DID learn it - here's proof"

**ROI:** 15 hours → $20K+ more per year = $1,300+ per hour

---

## 📝 Important Notes

- **Context Management:** This CLAUDE.md is intentionally short. Use links to access detailed docs when needed.
- **Cost:** ~$20-30/month (or $0 using free tiers)
- **Skills Gained:** K8s, GCP, Terraform, RAG systems, full-stack deployment

---

**Created:** November 2, 2025
**For:** Wipro AI/ML Platform Engineer role

**Now go build this and win that job.** 🚀
