# Project Architecture & Structure

**Last Updated:** November 3, 2025
**Architecture:** Distributed Microservices (4 services)

---

## 🏗️ Microservices Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              USER BROWSER                                    │
│                            vasukapoor.com                                    │
└─────────────────┬────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                       REACT FRONTEND (Vercel)                                │
│  Pages: Home │ Journey │ K8s │ GCP │ RAG │ Papers │ Analytics │ About        │
└──────┬───────────┬───────────────┬────────────────┬────────────────────────┬─┘
       │           │               │                │                        │
       │ HTTP      │ HTTP          │ HTTP           │ HTTP                   │ WS
       │           │               │                │                        │
       ▼           ▼               ▼                ▼                        ▼
┌──────────┐ ┌──────────┐  ┌──────────────┐ ┌────────────────┐ ┌──────────────────┐
│ Django   │ │ Scraper  │  │ Analytics    │ │ Doc Processor  │ │ Analytics        │
│ Backend  │ │ Service  │  │ Service      │ │ Service        │ │ (WebSocket)      │
│          │ │          │  │              │ │                │ │                  │
│ Cloud Run│ │Cloud Run │  │ Cloud Run    │ │ Cloud Run      │ │ Real-time events │
│ Port 8000│ │Port 8001 │  │ Port 8002    │ │ Port 8003      │ │                  │
└────┬─────┘ └────┬─────┘  └──────┬───────┘ └────────┬───────┘ └──────────────────┘
     │            │               │                   │
     │  Webhooks  │  POST papers  │  POST metrics     │  POST processed docs
     │◄───────────┤               │                   │
     │            │               │                   │
     │            │               ▼                   │
     │            │        ┌──────────────┐           │
     │            │        │    Redis     │◄──────────┤
     │            │        │ (Memorystore)│           │
     │            │        │              │           │
     │            │        │ - Metrics    │           │
     │            │        │ - Task Queue │           │
     │            │        └──────────────┘           │
     │            │                                    │
     ▼            ▼                                    ▼
┌────────────────────────────────────────────────────────────────┐
│                    SHARED RESOURCES                            │
│                                                                 │
│  ┌───────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │ Cloud SQL         │  │ ChromaDB       │  │ Cloud Storage│  │
│  │ PostgreSQL        │  │ Vector Store   │  │ PDF Storage  │  │
│  │                   │  │                │  │              │  │
│  │ - Portfolio Data  │  │ - Embeddings   │  │ - Papers     │  │
│  │ - Papers Metadata │  │ - RAG Docs     │  │ - Documents  │  │
│  │ - Jobs History    │  │                │  │              │  │
│  └───────────────────┘  └────────────────┘  └──────────────┘  │
└────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                      ┌────────────────────────────┐
                      │   Related Projects         │
                      │   Ringlet LMS (Azure AKS)  │
                      │   - Full K8s Deployment    │
                      │   - Terraform IaC          │
                      └────────────────────────────┘
```

---

## 🔧 Service Details

### 1️⃣ Django Backend Service
**URL:** `backend.vasukapoor.com` (Cloud Run)
**Technology:** Django 5.0 + DRF + ChromaDB + Vertex AI
**Port:** 8000

**Responsibilities:**
- Portfolio content API (tech stack, journey, projects)
- RAG chatbot (Vertex AI Gemini)
- User authentication
- Admin panel
- Database owner (PostgreSQL)
- Aggregates data from microservices

**Endpoints:**
```
GET  /api/tech-stack/
GET  /api/journey/
GET  /api/projects/
GET  /api/papers/          (proxies to Scraper Service)
GET  /api/chatbot/query/
POST /api/webhooks/scraper-complete
POST /api/webhooks/document-processed
```

---

### 2️⃣ Paper Scraper Service (NEW)
**URL:** `scraper.vasukapoor.com` (Cloud Run)
**Technology:** FastAPI + httpx + BeautifulSoup
**Port:** 8001

**Responsibilities:**
- Async scraping from arXiv, Hugging Face, Papers with Code
- Paper categorization & relevance scoring
- Tag extraction
- Scheduled jobs via Cloud Scheduler
- Webhook notifications to Django

**Endpoints:**
```
POST /scrape                 # Trigger scraping
GET  /scrape/status          # Job status
GET  /scrape/history         # Past jobs
GET  /health                 # Health check
```

**Scheduled Jobs:**
```yaml
Daily at 2 AM UTC: Scrape arXiv (last 1 day)
Weekly Sunday: Scrape HuggingFace + Papers with Code
```

---

### 3️⃣ Analytics Service (NEW)
**URL:** `analytics.vasukapoor.com` (Cloud Run)
**Technology:** Node.js + Express + Redis + Socket.io
**Port:** 8002

**Responsibilities:**
- Real-time event tracking (page views, clicks, searches)
- Popular papers tracking
- User engagement metrics
- WebSocket for live updates
- Geographic analytics

**Endpoints:**
```
POST /events/pageview        # Track page view
POST /events/click           # Track click
POST /events/search          # Track search
GET  /metrics/popular        # Popular papers
GET  /metrics/trending       # Trending topics
GET  /metrics/summary        # Overall stats
WS   /ws/realtime           # WebSocket endpoint
```

**Redis Data:**
```
analytics:pageviews:total    → Counter
analytics:papers:popular     → Sorted Set (by views)
analytics:realtime:users     → Set (active users)
```

---

### 4️⃣ Document Processor Service (NEW)
**URL:** `docs.vasukapoor.com` (Cloud Run)
**Technology:** FastAPI + Celery + PyPDF2 + ChromaDB
**Port:** 8003

**Responsibilities:**
- Download & parse PDFs
- Extract text from documents
- Generate embeddings (Vertex AI)
- Store in ChromaDB vector database
- Background processing via Celery
- Webhook notifications on completion

**Endpoints:**
```
POST /process/pdf            # Process PDF URL
POST /process/github         # Process GitHub repo
POST /process/text           # Process raw text
GET  /process/status/{id}    # Job status
GET  /jobs                   # All jobs
GET  /health                 # Health check
```

**Processing Pipeline:**
```
1. Receive PDF URL
2. Download PDF to Cloud Storage
3. Extract text (Celery task)
4. Chunk text (LangChain)
5. Generate embeddings (Vertex AI)
6. Store in ChromaDB
7. POST metadata to Django
8. Webhook on completion
```

---

## 🔗 Inter-Service Communication

### Service Discovery
All services use environment variables for URLs:
```bash
DJANGO_API_URL=https://backend.vasukapoor.com
SCRAPER_API_URL=https://scraper.vasukapoor.com
ANALYTICS_API_URL=https://analytics.vasukapoor.com
DOCPROCESSOR_API_URL=https://docs.vasukapoor.com
```

### Authentication
- **Service-to-Service:** Cloud Run IAM (service accounts)
- **Frontend-to-Services:** API keys (dev) → OAuth2 (production)

### Communication Patterns

**1. HTTP/REST (Synchronous)**
```
Frontend → Django: GET /api/papers
Django → Scraper: GET /scrape/status
Frontend → Analytics: POST /events/pageview
```

**2. Webhooks (Asynchronous)**
```
Scraper → Django: POST /api/webhooks/scraper-complete
  Payload: {source: "arxiv", papers_added: 25, job_id: "123"}

DocProcessor → Django: POST /api/webhooks/document-processed
  Payload: {doc_id: "456", status: "success", chunks: 42}
```

**3. WebSockets (Real-time)**
```
Frontend ↔ Analytics: WS /ws/realtime
  Events: {type: "pageview", page: "/papers", user_id: "anon-123"}
```

## Tech Stack

### Frontend
```
React 18 (Vite)
├── TailwindCSS (styling)
├── Framer Motion (animations)
├── React Router (navigation)
├── Axios (API calls)
└── React Markdown (content rendering)
```

### Backend
```
Django 5.0
├── Django REST Framework (API)
├── CORS Headers (frontend integration)
├── ChromaDB (vector store)
├── Vertex AI Gemini (LLM)
├── Cloud SQL PostgreSQL (production data)
├── ML/AI Paper Scraper
│   ├── arXiv API integration
│   ├── Hugging Face API
│   ├── Papers with Code scraper
│   └── Scheduled jobs (daily/weekly)
└── Whitenoise (static files)
```

### Deployment
```
Frontend → Vercel (vasukapoor.com)
         └── Auto-deploy on push to main
Backend → GCP Cloud Run (backend.vasukapoor.com)
         ├── RAG Service (integrated)
         └── ML Paper Scraper (background jobs)
Database → Cloud SQL PostgreSQL
         └── Region: us-central1
Related → Ringlet LMS (Azure AKS)
         └── /Users/vasukapoor/Jobs/practice/kub/ringlet/ringlet
```

### Infrastructure
```
Docker (containerization)
Terraform (IaC for GCP)
GitHub Actions (CI/CD)
GCP Cloud Build (alternative CI/CD)
```

## Project Structure

```
ai-platform-portfolio/
│
├── frontend/                      # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Footer.jsx
│   │   │   │   └── Layout.jsx
│   │   │   ├── sections/
│   │   │   │   ├── Hero.jsx
│   │   │   │   ├── JourneyTimeline.jsx
│   │   │   │   ├── SkillsMatrix.jsx
│   │   │   │   ├── TechStack.jsx
│   │   │   │   └── LiveDemos.jsx
│   │   │   ├── chatbot/
│   │   │   │   ├── ChatWidget.jsx
│   │   │   │   ├── ChatMessage.jsx
│   │   │   │   └── ChatInput.jsx
│   │   │   └── common/
│   │   │       ├── Button.jsx
│   │   │       ├── Card.jsx
│   │   │       └── CodeBlock.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Journey.jsx
│   │   │   ├── Kubernetes.jsx
│   │   │   ├── GCP.jsx
│   │   │   ├── RAG.jsx
│   │   │   ├── Terraform.jsx
│   │   │   ├── About.jsx
│   │   │   └── Blog.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── chatbot.js
│   │   ├── utils/
│   │   │   └── constants.js
│   │   ├── assets/
│   │   │   ├── images/
│   │   │   └── icons/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── README.md
│
├── backend/                       # Django application
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── portfolio/
│   │   ├── models.py             # Content models
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── rag_service/
│   │   ├── models.py
│   │   ├── vector_store.py       # ChromaDB integration
│   │   ├── embeddings.py
│   │   ├── chatbot.py            # RAG logic
│   │   ├── views.py
│   │   └── urls.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── manage.py
│   └── README.md
│
├── infrastructure/                # IaC and deployment
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   └── docker-compose.yml        # Local development
│
├── docs/                          # Documentation (RAG knowledge base)
│   ├── journey/
│   │   ├── 00-overview.md
│   │   ├── 01-kubernetes.md
│   │   ├── 02-gcp.md
│   │   ├── 03-terraform.md
│   │   └── 04-rag.md
│   ├── technical/
│   │   ├── architecture.md
│   │   ├── api-reference.md
│   │   └── deployment.md
│   ├── planning/
│   │   └── [planning docs]
│   └── blog/
│       ├── hour-1-2.md
│       ├── hour-3-4.md
│       └── ...
│
├── .github/
│   └── workflows/
│       ├── frontend-deploy.yml
│       └── backend-deploy.yml
│
├── CLAUDE.md
├── README.md
└── LICENSE
```

---

## ML/AI Paper Scraper Service

### Overview

The ML/AI Paper Scraper is an intelligent background service that automatically discovers, fetches, and curates the latest research papers, models, and techniques from the AI/ML community. It keeps the portfolio fresh with cutting-edge content and demonstrates real-world AI/ML platform engineering skills.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   ML/AI Paper Scraper                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Scraper Agent (Python)                    │    │
│  │                                                      │    │
│  │  ┌─────────────────┐  ┌─────────────────────────┐  │    │
│  │  │  Source Fetchers │  │  Content Processors     │  │    │
│  │  │                  │  │                         │  │    │
│  │  │  • arXiv API     │  │  • Metadata extraction  │  │    │
│  │  │  • HuggingFace   │  │  • Relevance scoring    │  │    │
│  │  │  • PapersWithCode│  │  • Deduplication        │  │    │
│  │  │  • Google Scholar│  │  • Categorization       │  │    │
│  │  └─────────────────┘  └─────────────────────────┘  │    │
│  │                                                      │    │
│  │  ┌─────────────────────────────────────────────┐   │    │
│  │  │         Filtering & Ranking                  │   │    │
│  │  │                                              │   │    │
│  │  │  • Relevance to AI/ML Platform Engineering  │   │    │
│  │  │  • Citation count                            │   │    │
│  │  │  • Publication date (recent)                 │   │    │
│  │  │  • Category matching (LLMs, RAG, MLOps, etc)│   │    │
│  │  └─────────────────────────────────────────────┘   │    │
│  └────────────────────────────────────────────────────┘    │
│                              │                               │
│                              ▼                               │
│  ┌────────────────────────────────────────────────────┐    │
│  │            Django Models (PostgreSQL)              │    │
│  │                                                      │    │
│  │  • Paper (title, abstract, authors, url, date)     │    │
│  │  • Category (LLMs, CV, NLP, MLOps, RAG, etc)       │    │
│  │  • ScraperJob (history, stats, last_run)           │    │
│  │  • PaperTag (keywords, techniques)                 │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Data Sources

**1. arXiv API**
- Focus: cs.AI, cs.LG, cs.CL categories
- Frequency: Daily scrape
- Fields: Title, abstract, authors, categories, publish date, PDF link

**2. Hugging Face Papers**
- Focus: Models, datasets, trending papers
- Frequency: Daily scrape
- Fields: Title, description, model card, likes, downloads

**3. Papers with Code**
- Focus: Papers with implementation code
- Frequency: Weekly scrape
- Fields: Title, abstract, GitHub repo, benchmarks, tasks

**4. Google Scholar Trends** (Optional)
- Focus: Trending AI/ML topics
- Frequency: Weekly scrape
- Fields: Search trends, citation velocity

### Django Models

**Paper Model:**
```python
class Paper(models.Model):
    CATEGORY_CHOICES = [
        ('llm', 'Large Language Models'),
        ('cv', 'Computer Vision'),
        ('rag', 'RAG & Embeddings'),
        ('mlops', 'MLOps & Platform'),
        ('training', 'Training & Optimization'),
        ('inference', 'Inference & Deployment'),
    ]

    title = models.CharField(max_length=500)
    abstract = models.TextField()
    authors = models.TextField()  # JSON list
    source = models.CharField(max_length=50)  # arxiv, huggingface, etc
    source_id = models.CharField(max_length=200, unique=True)
    url = models.URLField()
    pdf_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    published_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tags = models.JSONField(default=list)  # ["transformers", "attention", ...]
    citation_count = models.IntegerField(default=0)
    relevance_score = models.FloatField(default=0.0)  # 0-1 score
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**ScraperJob Model:**
```python
class ScraperJob(models.Model):
    source = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=20)  # running, completed, failed
    papers_found = models.IntegerField(default=0)
    papers_added = models.IntegerField(default=0)
    errors = models.TextField(blank=True)
```

### Scheduling

**Development:** Django management command
```bash
python manage.py scrape_papers --source arxiv --days 7
```

**Production:** Cloud Scheduler → Cloud Run Job
```yaml
# Cloud Scheduler configuration
schedule: "0 2 * * *"  # Daily at 2 AM UTC
target: scrape-papers-job
timeout: 30m
```

### API Endpoints

```
GET  /api/papers/                    # List all papers (paginated)
GET  /api/papers/?category=llm       # Filter by category
GET  /api/papers/?featured=true      # Featured papers only
GET  /api/papers/recent/             # Last 30 days
GET  /api/papers/trending/           # Sorted by citations + date
GET  /api/papers/{id}/               # Paper details
POST /api/papers/scrape/             # Trigger manual scrape (admin)
GET  /api/scraper-jobs/              # Scraper job history
```

### Frontend Display

**Papers Page (New):**
- Grid/list view of recent papers
- Filter by category, date range
- Sort by relevance, date, citations
- Quick view modal with abstract
- Links to PDF, arXiv, GitHub
- "Featured Papers" section
- Search functionality

**Home Page Integration:**
- "Latest Research" section
- 3-5 featured papers
- Auto-rotating carousel

### Benefits

**Portfolio Value:**
- Shows initiative and continuous learning
- Demonstrates API integration skills
- Proves ability to build background job systems
- Highlights ML/AI domain knowledge
- Creates dynamic, ever-updating content

**Interview Talking Points:**
- "I built an intelligent scraper that keeps me updated on latest AI/ML research"
- "It filters papers by relevance to platform engineering"
- "I can discuss current trends in LLMs, RAG, MLOps because my portfolio tracks them"
- "Shows I can build production-ready data pipelines"

### Implementation Priority

**Phase 1 (MVP - 2-3 hours):**
- Paper model
- arXiv scraper only
- Basic API endpoints
- Simple frontend list view

**Phase 2 (Full - 4-5 hours):**
- All data sources
- Relevance scoring
- Featured papers logic
- Advanced filtering/search
- Cloud Scheduler integration

**Phase 3 (Polish - 1-2 hours):**
- Deduplication logic
- Citation tracking
- Email digest (optional)
- Analytics dashboard
