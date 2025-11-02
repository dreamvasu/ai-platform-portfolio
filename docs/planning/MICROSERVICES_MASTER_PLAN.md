# Microservices Architecture - Master Plan

**Project:** AI/ML Platform Engineer Portfolio
**Date Created:** November 3, 2025
**Status:** Planning → Implementation

---

## 🎯 Vision

Transform the portfolio from a monolithic Django app into a **distributed microservices architecture** showcasing:
- Multi-language full-stack skills (Python, Node.js, React)
- Modern async frameworks (FastAPI, Express)
- Service-to-service communication
- Independent deployment & scaling
- Cloud-native patterns
- Real production architecture

---

## 📐 Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          vasukapoor.com                                  │
│                     React Frontend (Vercel)                              │
└────────┬────────────┬───────────────┬───────────────┬────────────────────┘
         │            │               │               │
         ▼            ▼               ▼               ▼
┌────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐
│  Django    │ │  Scraper    │ │ Analytics   │ │ Doc Processing      │
│  Backend   │ │  Service    │ │ Service     │ │ Service             │
│            │ │             │ │             │ │                     │
│ Cloud Run  │ │ Cloud Run   │ │ Cloud Run   │ │ Cloud Run           │
│ (Python)   │ │ (FastAPI)   │ │ (Node.js)   │ │ (FastAPI + Celery)  │
└─────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────────────┘
      │               │               │               │
      └───────────────┴───────────────┴───────────────┘
                      │
                      ▼
            ┌─────────────────────┐
            │  Cloud SQL          │
            │  PostgreSQL         │
            │  + Redis (Memstore) │
            └─────────────────────┘
```

---

## 🏗️ Microservices Breakdown

### 1. Django Backend (Main Service)
**Technology:** Django + DRF + ChromaDB + Vertex AI
**Port:** 8000
**Responsibilities:**
- Portfolio content API (tech stack, journey, projects)
- RAG chatbot service
- User authentication (future)
- Aggregating data from other services
- Admin interface
- PostgreSQL database owner

**Endpoints:**
- `/api/tech-stack/`
- `/api/journey/`
- `/api/projects/`
- `/api/papers/` (proxy to scraper service)
- `/api/chatbot/`
- `/api/analytics/` (proxy to analytics service)

---

### 2. Paper Scraper Service ⭐ NEW
**Technology:** FastAPI + httpx + Pydantic
**Port:** 8001
**Deployment:** Separate Cloud Run service
**Trigger:** Cloud Scheduler (daily 2 AM UTC)

**Responsibilities:**
- Scrape arXiv API (cs.AI, cs.LG, cs.CL)
- Scrape Hugging Face papers
- Scrape Papers with Code
- Categorize papers (LLM, RAG, MLOps, CV, etc.)
- Calculate relevance scores
- Extract tags and metadata
- POST results to Django backend API
- Maintain scraping job history

**Endpoints:**
```
POST   /scrape              # Trigger scraping (source, days)
GET    /scrape/status       # Current job status
GET    /scrape/history      # Past jobs
GET    /health              # Health check
POST   /scrape/arxiv        # Scrape arXiv only
POST   /scrape/huggingface  # Scrape HF only
POST   /scrape/pwc          # Scrape Papers with Code
```

**Features:**
- Async scraping (concurrent requests)
- Rate limiting (respect API limits)
- Retry logic with exponential backoff
- Progress tracking
- Error handling & logging
- Webhooks to Django on completion

**Tech Stack:**
```
FastAPI          # Web framework
httpx            # Async HTTP client
BeautifulSoup4   # HTML parsing
Pydantic         # Data validation
APScheduler      # Internal scheduling (optional)
feedparser       # RSS/Atom parsing
```

---

### 3. Analytics Service ⭐ NEW
**Technology:** Node.js + Express + Redis
**Port:** 8002
**Deployment:** Separate Cloud Run service
**Database:** Redis (Google Cloud Memorystore)

**Responsibilities:**
- Track page views (real-time)
- Popular papers tracking
- User engagement metrics
- Search queries tracking
- Geography data (IP-based)
- Real-time dashboards
- Export metrics to BigQuery (optional)

**Endpoints:**
```
POST   /events/pageview     # Track page view
POST   /events/click        # Track clicks
POST   /events/search       # Track searches
GET    /metrics/popular     # Most viewed papers
GET    /metrics/trending    # Trending topics
GET    /metrics/summary     # Overall stats
GET    /health              # Health check
WS     /ws/realtime         # WebSocket for live updates
```

**Metrics Tracked:**
```javascript
{
  pageViews: {
    total: 12543,
    unique: 3421,
    byPage: { "/": 4321, "/papers": 2134, ... }
  },
  papers: {
    mostViewed: [...],
    mostShared: [...],
    averageTimeOnPage: 45.2
  },
  searches: {
    topQueries: ["RAG", "LLM", "MLOps"],
    clickThroughRate: 0.73
  },
  geography: {
    countries: { "US": 4521, "IN": 3210, ... }
  },
  realtime: {
    activeUsers: 12,
    currentPages: [...]
  }
}
```

**Tech Stack:**
```
Node.js          # Runtime
Express          # Web framework
Redis            # Fast in-memory storage
Socket.io        # WebSockets
node-cache       # In-memory caching
axios            # HTTP client
geoip-lite       # IP geolocation
```

---

### 4. Document Processing Service ⭐ NEW
**Technology:** FastAPI + Celery + Redis
**Port:** 8003
**Deployment:** Cloud Run + Cloud Tasks
**Queue:** Redis (task queue)

**Responsibilities:**
- Download PDFs from arXiv/URLs
- Extract text from PDFs (PyPDF2, pdfplumber)
- Generate embeddings for RAG
- Chunk documents intelligently
- Store in vector database (ChromaDB)
- Process GitHub README files
- Generate summaries (Vertex AI)

**Endpoints:**
```
POST   /process/pdf         # Process PDF URL
POST   /process/github      # Process GitHub repo
POST   /process/text        # Process raw text
GET    /process/status/{id} # Job status
GET    /jobs                # List all jobs
GET    /health              # Health check
```

**Workflow:**
```
1. Receive document URL/text
2. Download/validate document
3. Extract text (async Celery task)
4. Chunk text (recursive character splitter)
5. Generate embeddings (Vertex AI)
6. Store in ChromaDB
7. POST metadata to Django
8. Notify completion via webhook
```

**Features:**
- Async processing (Celery workers)
- Support for PDF, TXT, MD, GitHub repos
- Smart chunking (preserve context)
- Duplicate detection
- Batch processing
- Progress tracking

**Tech Stack:**
```
FastAPI          # Web framework
Celery           # Distributed task queue
Redis            # Task broker
PyPDF2           # PDF parsing
pdfplumber       # Advanced PDF extraction
chromadb         # Vector database
langchain        # Text splitting
google-cloud-ai  # Vertex AI embeddings
```

---

## 📊 Database Strategy

### PostgreSQL (Cloud SQL)
**Owner:** Django Backend
**Tables:**
- TechStack, JourneyEntry, Project (Django)
- Paper, ScraperJob (Django - synced from Scraper Service)
- ProcessingJob (Django - synced from Doc Service)

### Redis (Memorystore)
**Users:**
- Analytics Service (primary - metrics storage)
- Document Processing Service (Celery task queue)

**Data Structure:**
```redis
# Analytics
analytics:pageviews:total -> counter
analytics:pageviews:2025-11-03 -> hash
analytics:papers:popular -> sorted set
analytics:realtime:users -> set

# Celery
celery:tasks:pending -> list
celery:tasks:results -> hash
```

### ChromaDB (Vector Store)
**Owner:** Document Processing Service
**Writer:** Document Processing Service
**Reader:** Django Backend (RAG queries)

---

## 🔄 Inter-Service Communication

### Service Discovery
- Environment variables with service URLs
- Cloud Run service-to-service authentication

### Communication Patterns

**1. Synchronous (REST API)**
```
Frontend → Django: GET /api/papers
Django → Scraper: GET /scrape/status
Frontend → Analytics: POST /events/pageview
```

**2. Asynchronous (Webhooks)**
```
Scraper → Django: POST /api/webhooks/scraper-complete
DocProcessor → Django: POST /api/webhooks/document-processed
```

**3. Real-time (WebSockets)**
```
Frontend ↔ Analytics: WS /ws/realtime
```

### Authentication
- Service-to-service: JWT tokens or Cloud Run IAM
- Frontend-to-services: API keys (development) → OAuth (production)

---

## 🚀 Deployment Strategy

### Cloud Run Services
```
1. portfolio-backend       (Django)       - backend.vasukapoor.com
2. portfolio-scraper       (FastAPI)      - scraper.vasukapoor.com
3. portfolio-analytics     (Node.js)      - analytics.vasukapoor.com
4. portfolio-docprocessor  (FastAPI)      - docs.vasukapoor.com
```

### Cloud Scheduler Jobs
```
scraper-daily-job:
  schedule: "0 2 * * *"  # 2 AM UTC daily
  target: portfolio-scraper
  endpoint: /scrape
  payload: {"source": "all", "days": 1}
```

### Shared Resources
```
- Cloud SQL PostgreSQL (shared database)
- Memorystore Redis (shared cache)
- Cloud Storage (PDF storage, static files)
- Vertex AI (shared LLM/embeddings)
```

---

## 📁 Project Structure

```
ai-platform-portfolio/
│
├── frontend/                        # React (Vercel)
│   └── src/
│       └── services/
│           ├── django-api.js
│           ├── scraper-api.js
│           ├── analytics-api.js
│           └── docprocessor-api.js
│
├── backend/                         # Django (Cloud Run)
│   ├── portfolio/
│   ├── rag_service/
│   └── Dockerfile
│
├── services/
│   ├── scraper/                     # FastAPI
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── scrapers/
│   │   │   │   ├── arxiv.py
│   │   │   │   ├── huggingface.py
│   │   │   │   └── paperswithcode.py
│   │   │   ├── models.py
│   │   │   └── utils.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── analytics/                   # Node.js
│   │   ├── src/
│   │   │   ├── server.js
│   │   │   ├── routes/
│   │   │   ├── services/
│   │   │   └── utils/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── README.md
│   │
│   └── document-processor/          # FastAPI + Celery
│       ├── app/
│       │   ├── main.py
│       │   ├── tasks.py
│       │   ├── processors/
│       │   └── utils.py
│       ├── Dockerfile
│       ├── requirements.txt
│       └── README.md
│
├── docs/
│   └── planning/
│       ├── MICROSERVICES_MASTER_PLAN.md  # This file
│       ├── MICROSERVICES_TRACKER.md      # Implementation tracker
│       └── architecture.md               # Updated architecture
│
└── infrastructure/
    ├── docker-compose.yml           # Local development
    └── kubernetes/                   # K8s manifests (future)
```

---

## ⏱️ Implementation Timeline

### Phase 1: Planning & Setup (2 hours) ✅ IN PROGRESS
- [x] Create master plan
- [ ] Create implementation tracker
- [ ] Update architecture docs
- [ ] Setup service directories

### Phase 2: Paper Scraper Service (4-5 hours)
- [ ] FastAPI boilerplate
- [ ] arXiv scraper (migrate from Django)
- [ ] Hugging Face scraper
- [ ] Papers with Code scraper
- [ ] API endpoints
- [ ] Dockerfile
- [ ] Deploy to Cloud Run
- [ ] Test integration with Django

### Phase 3: Analytics Service (4-5 hours)
- [ ] Express.js boilerplate
- [ ] Redis connection
- [ ] Event tracking endpoints
- [ ] Metrics calculation
- [ ] WebSocket setup
- [ ] Dockerfile
- [ ] Deploy to Cloud Run
- [ ] Frontend integration

### Phase 4: Document Processor Service (5-6 hours)
- [ ] FastAPI + Celery boilerplate
- [ ] PDF processing
- [ ] Text extraction
- [ ] Embedding generation
- [ ] ChromaDB integration
- [ ] Dockerfile
- [ ] Deploy to Cloud Run
- [ ] Setup Cloud Tasks

### Phase 5: Integration (3-4 hours)
- [ ] Service-to-service auth
- [ ] Webhook endpoints
- [ ] Frontend updates
- [ ] End-to-end testing
- [ ] Performance testing

### Phase 6: Deployment & Polish (2-3 hours)
- [ ] Cloud Scheduler setup
- [ ] Monitoring/logging
- [ ] Documentation
- [ ] Demo video

**TOTAL: 20-25 hours**

---

## 💡 Interview Talking Points

**"I built a distributed microservices architecture with 4 independently deployed services"**

1. **Polyglot Architecture**: Python (Django, FastAPI) + Node.js
2. **Async Patterns**: FastAPI async/await, Node.js event loop
3. **Service Communication**: REST, WebSockets, Webhooks
4. **Cloud Native**: All services on Cloud Run, auto-scaling
5. **Task Queues**: Celery with Redis broker
6. **Real-time**: WebSocket analytics, live dashboards
7. **Independent Deployment**: Each service has CI/CD pipeline
8. **Observability**: Health checks, logging, metrics

---

## 🎯 Success Metrics

- [ ] 4 services deployed and running
- [ ] Sub-200ms latency for all APIs
- [ ] Scraper processes 100+ papers daily
- [ ] Analytics tracks 1000+ events/day
- [ ] Document processor handles 50+ PDFs/day
- [ ] 99.9% uptime for all services
- [ ] Complete API documentation (Swagger/OpenAPI)

---

## 📚 Tech Stack Summary

| Service | Language | Framework | Database | Queue | Deploy |
|---------|----------|-----------|----------|-------|--------|
| Frontend | JavaScript | React + Vite | - | - | Vercel |
| Backend | Python 3.11 | Django + DRF | PostgreSQL | - | Cloud Run |
| Scraper | Python 3.11 | FastAPI | PostgreSQL | - | Cloud Run |
| Analytics | Node.js 20 | Express | Redis | - | Cloud Run |
| Doc Processor | Python 3.11 | FastAPI + Celery | PostgreSQL | Redis | Cloud Run |

---

**Ready to build! Let's crush this microservices architecture! 🚀**
