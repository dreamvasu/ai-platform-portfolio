# Project Architecture & Structure

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                              │
│                   yourdomain.com                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               REACT FRONTEND (Vercel)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Landing  │  Journey  │  Tech Dives  │  About  │Blog │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                   │
│                  ┌───────┴────────┐                          │
│                  ▼                ▼                          │
│          [Content API]    [RAG Chatbot API]                 │
└─────────────────┬────────────────┬───────────────────────────┘
                  │                │
                  ▼                ▼
┌──────────────────────┐  ┌─────────────────────────────────┐
│  DJANGO BACKEND      │  │  RAG SERVICE                    │
│  (GCP Cloud Run)     │  │  (GCP Cloud Run)                │
│                      │  │                                 │
│  ┌────────────────┐ │  │  ┌──────────────────────────┐   │
│  │ REST API       │ │  │  │ Vector DB (ChromaDB)     │   │
│  │ Content CRUD   │ │  │  │ LLM (OpenAI/Vertex AI)   │   │
│  │ Admin Panel    │ │  │  │ Document Processing      │   │
│  └────────────────┘ │  │  └──────────────────────────┘   │
│                      │  │                                 │
│  ┌────────────────┐ │  │  Knowledge Base:                │
│  │ PostgreSQL     │ │  │  - Your documentation           │
│  │ Cloud SQL      │ │  │  - GitHub commits               │
│  └────────────────┘ │  │  - Learning logs                │
└──────────────────────┘  └─────────────────────────────────┘
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
├── ChromaDB / Pinecone (vector store)
├── OpenAI / Vertex AI (LLM)
├── Postgres / SQLite (data)
└── Whitenoise (static files)
```

### Deployment
```
Frontend → Vercel / Netlify (free tier)
Backend → GCP Cloud Run (shows GCP skills)
RAG API → GCP Cloud Run (separate service)
Database → Cloud SQL / Firestore
Domain → Custom domain (optional)
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
