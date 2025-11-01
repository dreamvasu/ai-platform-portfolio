# AI/ML PLATFORM ENGINEER PORTFOLIO - COMPLETE BUILD PLAN

**Project Name:** "The 12-Hour Sprint - Journey to AI Platform Engineering"  
**Created:** November 2, 2025  
**Builder:** Vasu Kapoor  
**Purpose:** Build a living portfolio that proves learning velocity and technical depth  
**Timeline:** 14-16 hours total build time  
**Deploy Target:** GCP (Cloud Run) + Vercel/Netlify  

---

## 🎯 PROJECT VISION

### **The Big Idea**

Build a **self-documenting portfolio** that showcases your 12-hour sprint journey from 65% match to 90%+ match for the Wipro AI/ML Platform Engineer role.

**This isn't just a portfolio - it's a proof system:**
- ✅ Proves fast learning (the sprint itself)
- ✅ Proves full-stack skills (React + Django)
- ✅ Proves AI/ML skills (RAG chatbot)
- ✅ Proves platform skills (K8s, GCP, IaC)
- ✅ Proves shipping ability (live deployment)

### **The Killer Feature**

**RAG-powered chatbot that answers questions about YOUR journey using YOUR documentation as the knowledge base.**

Interviewer can literally ask:
- "How did Vasu learn Kubernetes?"
- "What's his GCP experience?"
- "Show me proof of his deployments"

And get AI-powered answers from your actual documentation. **Mind = blown.** 🤯

---

## 📊 TECH STACK

### **Frontend**
```
React 18 (Vite)
├── TailwindCSS (styling)
├── Framer Motion (animations)
├── React Router (navigation)
├── Axios (API calls)
└── React Markdown (content rendering)
```

### **Backend**
```
Django 5.0
├── Django REST Framework (API)
├── CORS Headers (frontend integration)
├── ChromaDB / Pinecone (vector store)
├── OpenAI / Vertex AI (LLM)
├── Postgres / SQLite (data)
└── Whitenoise (static files)
```

### **Deployment**
```
Frontend → Vercel / Netlify (free tier)
Backend → GCP Cloud Run (shows GCP skills)
RAG API → GCP Cloud Run (separate service)
Database → Cloud SQL / Firestore
Domain → Custom domain (optional)
```

### **Infrastructure**
```
Docker (containerization)
Terraform (IaC for GCP)
GitHub Actions (CI/CD)
GCP Cloud Build (alternative CI/CD)
```

---

## 🏗️ PROJECT ARCHITECTURE

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

---

## 📁 PROJECT STRUCTURE

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
├── README.md
└── LICENSE
```

---

## 🎨 FRONTEND PAGES BREAKDOWN

### **1. Home / Landing Page**

**Purpose:** Hook them in 3 seconds

**Sections:**
```jsx
<Hero>
  - Headline: "From 65% Match to 90% Match in 12 Hours"
  - Subheadline: "How I transformed into an AI Platform Engineer"
  - CTA: [View Journey] [Live Demos] [GitHub]
  - Animated background with tech stack icons
</Hero>

<StatsSection>
  - Technologies Mastered: 8
  - Hours Invested: 12
  - GitHub Commits: 50+
  - Live Deployments: 3
</StatsSection>

<JourneyPreview>
  - Timeline visualization (animated)
  - Before/After skills comparison
  - Key achievements
</JourneyPreview>

<TechStackShowcase>
  - Interactive tech stack grid
  - Hover for details
  - Links to deep dive pages
</TechStackShowcase>

<LiveDemosSection>
  - Embedded RAG chatbot
  - K8s deployment screenshots
  - GCP Cloud Run metrics
  - Interactive architecture diagram
</LiveDemosSection>

<CTASection>
  - "Ready to see how I did it?"
  - Link to full journey
</CTASection>
```

---

### **2. Journey Page**

**Purpose:** Tell the complete story

**Layout:**
```jsx
<TimelineView>
  Hour 0: The Challenge
  - Job requirements analysis
  - Gap identification
  - Decision to sprint
  
  Hour 1-2: Kubernetes Fundamentals
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways
  
  Hour 3-4: GCP Cloud Run
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways
  
  Hour 5-6: Infrastructure as Code
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways
  
  Hour 7-8: RAG System
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways
  
  Hour 9-10: Integration & Testing
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways
  
  Hour 11-12: Deployment & Documentation
  - What I learned
  - What I built
  - Challenges faced
  - Key takeaways
</TimelineView>

<SkillsEvolution>
  - Before sprint skills matrix
  - After sprint skills matrix
  - Visual comparison
</SkillsEvolution>

<GitHubActivity>
  - Commit history visualization
  - Code snippets
  - Links to repos
</GitHubActivity>
```

---

### **3. Technical Deep Dive Pages**

Create separate pages for each major tech:

**A. Kubernetes Deep Dive**
```jsx
<Overview>
  - What is Kubernetes
  - Why it matters for AI/ML platforms
  - My learning approach
</Overview>

<Implementation>
  - Architecture diagram
  - Code snippets (YAML files)
  - Deployment process
  - Troubleshooting stories
</Implementation>

<Results>
  - Screenshots of running cluster
  - kubectl commands used
  - Performance metrics
  - Lessons learned
</Results>

<Resources>
  - Links to docs I used
  - GitHub repo link
  - Commands cheat sheet
</Resources>
```

**B. GCP Deep Dive**
```jsx
<Overview>
  - GCP services used (Cloud Run, Vertex AI)
  - Architecture decisions
  - Cost considerations
</Overview>

<Implementation>
  - Step-by-step deployment guide
  - gcloud commands used
  - Configuration screenshots
  - Integration with Vertex AI
</Implementation>

<Results>
  - Live deployment URL
  - Performance metrics
  - Auto-scaling demos
  - Cost analysis
</Results>
```

**C. RAG System Deep Dive**
```jsx
<Overview>
  - RAG architecture
  - Tech stack (ChromaDB, OpenAI)
  - Use case for portfolio
</Overview>

<Implementation>
  - Vector database setup
  - Embedding generation
  - Query flow
  - Code walkthrough
</Implementation>

<Demo>
  - Live chatbot embedded
  - Example queries
  - Response quality showcase
</Demo>

<Technical>
  - API endpoints
  - Request/response format
  - Performance optimization
</Technical>
```

**D. Terraform / IaC Deep Dive**
```jsx
<Overview>
  - Infrastructure as Code principles
  - Why Terraform
  - Resources managed
</Overview>

<Implementation>
  - Terraform code walkthrough
  - GCP resources provisioned
  - State management
  - Modules used
</Implementation>

<Results>
  - Infrastructure diagram
  - terraform plan output
  - Cost estimation
  - Reproducibility demo
</Results>
```

---

### **4. About Page**

**Purpose:** Professional profile + personal story

```jsx
<Introduction>
  - Photo
  - Elevator pitch
  - Current role & experience
</Introduction>

<Background>
  - 10 years software architecture
  - Key achievements
  - Industries worked in
  - Technologies mastered
</Background>

<WhyThisRole>
  - Career transition story
  - Why AI/ML platform engineering
  - What excites you
  - What you bring
</WhyThisRole>

<Resume>
  - Download button
  - Key highlights
  - Work history timeline
</Resume>

<Contact>
  - LinkedIn
  - GitHub
  - Email
  - Portfolio chatbot CTA
</Contact>
```

---

### **5. Blog / Learning Log (Optional but Powerful)**

**Purpose:** Show thought process and learning journey

```jsx
Posts structure:
- "Hour 1-2: Breaking into Kubernetes"
- "Hour 3-4: GCP Cloud Run - First Impressions"
- "Hour 5-6: Infrastructure as Code Mindset Shift"
- "Hour 7-8: Building a Production-Ready RAG System"
- "Hour 9-10: The Integration Hell and How I Survived"
- "Hour 11-12: Shipping to Production"
- "Lessons Learned: What I'd Do Differently"
- "From Application Dev to Platform Engineer"
```

---

## 🤖 RAG CHATBOT IMPLEMENTATION

### **Knowledge Base Structure**

```python
# docs/knowledge_base.py

KNOWLEDGE_SOURCES = [
    {
        "type": "markdown",
        "path": "docs/journey/",
        "metadata": {
            "category": "journey",
            "tags": ["learning", "timeline", "sprint"]
        }
    },
    {
        "type": "markdown",
        "path": "docs/technical/",
        "metadata": {
            "category": "technical",
            "tags": ["architecture", "api", "deployment"]
        }
    },
    {
        "type": "code",
        "path": "backend/",
        "metadata": {
            "category": "code",
            "tags": ["django", "python", "api"]
        }
    },
    {
        "type": "code",
        "path": "frontend/src/",
        "metadata": {
            "category": "code",
            "tags": ["react", "javascript", "frontend"]
        }
    },
    {
        "type": "infrastructure",
        "path": "infrastructure/",
        "metadata": {
            "category": "infrastructure",
            "tags": ["terraform", "kubernetes", "deployment"]
        }
    }
]
```

### **RAG Service Architecture**

```python
# backend/rag_service/chatbot.py

class PortfolioChatbot:
    """
    RAG-powered chatbot that answers questions about
    Vasu's learning journey and technical implementations.
    """
    
    def __init__(self):
        self.vector_store = ChromaDB()
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4")
        
    def ingest_documentation(self):
        """
        Load all documentation into vector store
        """
        for source in KNOWLEDGE_SOURCES:
            documents = self.load_documents(source)
            chunks = self.chunk_documents(documents)
            embeddings = self.embeddings.embed_documents(chunks)
            self.vector_store.add(chunks, embeddings, source.metadata)
    
    def query(self, question: str, context: dict = None):
        """
        Answer questions using RAG
        """
        # Get relevant context
        relevant_docs = self.vector_store.similarity_search(
            question, 
            k=5
        )
        
        # Build prompt
        prompt = self.build_prompt(question, relevant_docs, context)
        
        # Generate answer
        response = self.llm(prompt)
        
        # Add sources
        return {
            "answer": response,
            "sources": [doc.metadata for doc in relevant_docs],
            "confidence": self.calculate_confidence(relevant_docs)
        }
    
    def build_prompt(self, question, docs, context):
        """
        Build RAG prompt
        """
        return f"""
        You are an AI assistant helping visitors learn about Vasu Kapoor's
        journey to becoming an AI/ML Platform Engineer.
        
        Context from Vasu's documentation:
        {self.format_docs(docs)}
        
        Question: {question}
        
        Instructions:
        - Answer based ONLY on the provided context
        - Be specific and cite relevant parts of the journey
        - Include links to relevant GitHub repos or pages
        - If you don't know, say so
        - Keep answers concise but informative
        
        Answer:
        """
```

### **Sample Chatbot Interactions**

```
User: "How did Vasu learn Kubernetes?"

Bot: "Vasu learned Kubernetes during hours 1-2 of his 12-hour sprint. 
He focused on core concepts: Pods, Deployments, Services, and HPA. 
His approach was hands-on - he built a working RAG API deployment 
with autoscaling and load balancing.

Key achievements:
✅ Deployed microservice to Minikube
✅ Implemented horizontal pod autoscaling
✅ Set up ingress and load balancing
✅ Wrote K8s manifests from scratch

You can see his implementation here: [GitHub link]
And read his detailed journey here: [Journey page link]"

---

User: "What's Vasu's experience with GCP?"

Bot: "Vasu has production experience with Azure and recently gained 
hands-on GCP experience during his 12-hour sprint.

GCP technologies he used:
✅ Cloud Run (serverless containers)
✅ Vertex AI (managed ML services)
✅ Cloud SQL (managed database)
✅ Cloud Build (CI/CD)

He deployed 2 production services to GCP:
1. Django backend API (Cloud Run)
2. RAG chatbot service (Cloud Run)

Both are live and auto-scaling. Try the demo: [Live URL]
Architecture details: [GCP Deep Dive page]"

---

User: "Show me proof of his deployments"

Bot: "Here's proof of Vasu's live deployments:

🚀 GCP Cloud Run Services:
- Backend API: [URL]
- RAG Service: [URL]
- Status: ✅ Running (uptime: 99.9%)

🎯 Kubernetes Cluster:
- GitHub: [K8s manifests repo]
- Screenshots: [Deployments page]
- Commands used: [Documentation]

📦 Infrastructure as Code:
- Terraform configs: [GitHub repo]
- Resources provisioned: 12 GCP resources
- Cost: ~$20/month with auto-scaling

All code is open source and deployable. Check the 
repositories to verify the implementations!"
```

---

## 🎯 IMPLEMENTATION PHASES

### **PHASE 1: FOUNDATION (4-5 hours)**

**1.1 Project Setup (1 hour)**
```bash
# Frontend
npm create vite@latest frontend -- --template react
cd frontend
npm install tailwindcss framer-motion react-router-dom axios react-markdown

# Backend
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate
pip install django djangorestframework django-cors-headers
django-admin startproject core .
python manage.py startapp portfolio
python manage.py startapp rag_service

# Infrastructure
mkdir -p infrastructure/{terraform,kubernetes}
```

**1.2 Basic Frontend Structure (2 hours)**
- Set up React Router
- Create layout components (Navbar, Footer)
- Build landing page with hero section
- Add basic styling with Tailwind
- Implement responsive design

**1.3 Basic Backend API (1.5 hours)**
- Set up Django REST Framework
- Create content models
- Build CRUD API endpoints
- Configure CORS
- Add Django admin panel

**1.4 Local Development Setup (0.5 hour)**
- Docker Compose for local dev
- Environment variables setup
- Database configuration
- API integration test

---

### **PHASE 2: CONTENT CREATION (4-5 hours)**

**2.1 Documentation Writing (2 hours)**
- Write journey timeline content
- Create technical deep dive pages
- Document learning process
- Add code snippets and examples
- Create architecture diagrams

**2.2 Frontend Pages Implementation (2 hours)**
- Journey page with timeline
- Technical deep dive pages
- About page
- Blog posts (if doing)
- Navigation between pages

**2.3 Visual Assets (1 hour)**
- Architecture diagrams (use Excalidraw/Figma)
- Screenshots of deployments
- Code snippet formatting
- Icons and images
- Responsive image handling

---

### **PHASE 3: RAG CHATBOT (3-4 hours)**

**3.1 Vector Store Setup (1 hour)**
```python
# backend/rag_service/vector_store.py

from chromadb import Client
from chromadb.config import Settings

class VectorStore:
    def __init__(self):
        self.client = Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        self.collection = self.client.get_or_create_collection(
            name="portfolio_docs",
            metadata={"description": "Vasu's portfolio documentation"}
        )
    
    def add_documents(self, documents, embeddings, metadatas):
        """Add documents to vector store"""
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=[f"doc_{i}" for i in range(len(documents))]
        )
    
    def search(self, query_embedding, k=5):
        """Search for similar documents"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results
```

**3.2 Document Ingestion (1 hour)**
```python
# backend/rag_service/ingest.py

import os
from pathlib import Path
from openai import OpenAI

class DocumentIngestion:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.client = OpenAI()
    
    def ingest_markdown_files(self, directory):
        """Ingest all markdown files from directory"""
        docs_path = Path(directory)
        
        for md_file in docs_path.rglob("*.md"):
            with open(md_file, 'r') as f:
                content = f.read()
            
            # Chunk the document
            chunks = self.chunk_text(content)
            
            # Generate embeddings
            embeddings = self.generate_embeddings(chunks)
            
            # Store in vector database
            metadatas = [{
                "source": str(md_file),
                "chunk_id": i,
                "total_chunks": len(chunks)
            } for i in range(len(chunks))]
            
            self.vector_store.add_documents(
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas
            )
    
    def chunk_text(self, text, chunk_size=500, overlap=50):
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    def generate_embeddings(self, texts):
        """Generate embeddings using OpenAI"""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        return [item.embedding for item in response.data]
```

**3.3 RAG Query Implementation (1 hour)**
```python
# backend/rag_service/chatbot.py

from openai import OpenAI

class RAGChatbot:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.client = OpenAI()
    
    def query(self, question: str):
        """Answer question using RAG"""
        # Generate query embedding
        query_embedding = self.generate_embedding(question)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, k=5)
        
        # Build context from results
        context = "\n\n".join(results['documents'][0])
        
        # Generate answer
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are an AI assistant helping visitors 
                    learn about Vasu Kapoor's journey to becoming an AI/ML 
                    Platform Engineer. Answer based ONLY on the provided 
                    context. Be specific, cite sources, and include relevant 
                    links. If you don't know, say so."""
                },
                {
                    "role": "user",
                    "content": f"""Context: {context}
                    
                    Question: {question}
                    
                    Answer:"""
                }
            ]
        )
        
        return {
            "answer": response.choices[0].message.content,
            "sources": results['metadatas'][0],
            "context_used": len(results['documents'][0])
        }
    
    def generate_embedding(self, text):
        """Generate embedding for text"""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
```

**3.4 Frontend Chatbot Widget (1 hour)**
```jsx
// frontend/src/components/chatbot/ChatWidget.jsx

import { useState } from 'react';
import axios from 'axios';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hi! I'm Vasu's AI assistant. Ask me anything about his journey to AI/ML Platform Engineering!"
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Call RAG API
      const response = await axios.post('/api/chatbot/query/', {
        question: input
      });

      // Add assistant response
      const assistantMessage = {
        role: 'assistant',
        content: response.data.answer,
        sources: response.data.sources
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chatbot error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Chat button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-600 text-white rounded-full p-4 shadow-lg hover:bg-blue-700"
        >
          💬 Ask Me Anything
        </button>
      )}

      {/* Chat window */}
      {isOpen && (
        <div className="bg-white rounded-lg shadow-2xl w-96 h-[500px] flex flex-col">
          {/* Header */}
          <div className="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
            <h3 className="font-bold">Vasu's AI Assistant</h3>
            <button onClick={() => setIsOpen(false)}>✕</button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`${
                  msg.role === 'user' ? 'text-right' : 'text-left'
                }`}
              >
                <div
                  className={`inline-block p-3 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  {msg.content}
                </div>
                {msg.sources && (
                  <div className="text-xs text-gray-500 mt-1">
                    Sources: {msg.sources.length} documents
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="text-left">
                <div className="inline-block p-3 rounded-lg bg-gray-100">
                  Thinking...
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="p-4 border-t">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Ask about Vasu's journey..."
                className="flex-1 border rounded-lg px-3 py-2"
              />
              <button
                onClick={sendMessage}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

---

### **PHASE 4: DEPLOYMENT (2-3 hours)**

**4.1 Backend Deployment to GCP (1 hour)**
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

```bash
# Deploy to Cloud Run
gcloud run deploy portfolio-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="DJANGO_SETTINGS_MODULE=core.settings" \
  --memory=2Gi \
  --cpu=2
```

**4.2 Frontend Deployment to Vercel (0.5 hour)**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

**4.3 Infrastructure as Code (1 hour)**
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

**4.4 CI/CD Pipeline (0.5 hour)**
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

---

### **PHASE 5: POLISH & OPTIMIZATION (2 hours)**

**5.1 Performance Optimization (0.5 hour)**
- Image optimization
- Code splitting
- Lazy loading
- Caching strategies
- Lighthouse audit

**5.2 SEO & Meta Tags (0.5 hour)**
```jsx
// frontend/src/components/SEO.jsx

import { Helmet } from 'react-helmet-async';

export default function SEO({ 
  title, 
  description, 
  image,
  url 
}) {
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

**5.3 Analytics & Monitoring (0.5 hour)**
- Google Analytics setup
- Error tracking (Sentry)
- Performance monitoring
- User behavior tracking

**5.4 Final Testing (0.5 hour)**
- Cross-browser testing
- Mobile responsiveness
- API endpoint testing
- Chatbot functionality
- Load testing

---

## 📊 SUCCESS METRICS

### **Technical Metrics**
- ✅ Frontend deployed and accessible
- ✅ Backend API responding < 200ms
- ✅ RAG chatbot accuracy > 85%
- ✅ Mobile responsive (100% score)
- ✅ Lighthouse score > 90
- ✅ Zero console errors
- ✅ All links working

### **Content Metrics**
- ✅ Complete journey documentation
- ✅ 4+ technical deep dives
- ✅ 50+ GitHub commits
- ✅ 10+ architecture diagrams
- ✅ Live deployment proof

### **Impact Metrics**
- ✅ Wipro job application submitted
- ✅ Portfolio URL in resume
- ✅ LinkedIn post published
- ✅ GitHub repo public
- ✅ Chatbot tested and working

---

## 🎯 USING THE PORTFOLIO IN JOB APPLICATION

### **Resume Update**
```
Portfolio: vasukapoor-ai-platform.com
GitHub: github.com/yourusername/ai-platform-portfolio

AI/ML Platform Engineering Sprint (Nov 2025)
• Built production RAG system deployed to GCP Cloud Run
• Implemented Kubernetes deployments with autoscaling
• Created Infrastructure as Code with Terraform
• Documented 12-hour learning sprint in interactive portfolio
• Tech Stack: React, Django, K8s, GCP, Terraform, ChromaDB
```

### **LinkedIn Post Template**
```
🚀 From 65% Match to 90% Match in 12 Hours

I just completed an intense learning sprint to transform myself 
into an AI/ML Platform Engineer.

What I built:
✅ Production RAG system
✅ Kubernetes deployments
✅ GCP Cloud Run services
✅ Infrastructure as Code (Terraform)
✅ Interactive portfolio with AI chatbot

The best part? Everything is live and documented.

Portfolio: [your-domain.com]
GitHub: [repo-link]

This is what learning velocity looks like. 💪

#AIEngineering #Kubernetes #GCP #MachineLearning #CareerGrowth
```

### **Cover Letter Hook**
```
Dear Hiring Manager,

When I saw the Wipro AI/ML Platform Engineer role, I identified a 
gap in my Kubernetes and GCP experience. Rather than just claim 
"I can learn it," I spent 12 hours proving it.

I built a production RAG system, deployed it to Kubernetes and GCP 
Cloud Run, and documented the entire journey in an interactive 
portfolio with an AI-powered chatbot.

You can explore everything at [portfolio-url].

This demonstrates not just technical skills, but the learning 
velocity your team needs in a rapidly evolving AI landscape.
```

### **Email to Recruiter**
```
Subject: AI/ML Platform Engineer - Portfolio Submission

Hi [Recruiter Name],

I'm applying for the AI/ML Platform Engineer role (Ref: [Job ID]).

I noticed the role emphasizes Kubernetes, GCP, and IaC - technologies 
I recently mastered through an intensive learning sprint. Rather than 
just list these on my resume, I built a complete portfolio demonstrating 
my hands-on experience:

🔗 Portfolio: [your-domain.com]
🔗 GitHub: [repo-link]
📄 Resume: [attached]

The portfolio includes:
- Live RAG system on GCP
- Kubernetes deployment with autoscaling
- Terraform infrastructure code
- Interactive AI chatbot (try asking it about my experience!)

I'd love to discuss how my rapid learning ability and technical depth 
can contribute to Citi's AI platform.

Best regards,
Vasu Kapoor
[contact info]
```

---

## 🎤 INTERVIEW TALKING POINTS

### **Opening Statement**
> "I built this portfolio specifically to demonstrate my learning 
> velocity. When I saw your Kubernetes and GCP requirements, I didn't 
> just read documentation - I built production deployments. Let me show 
> you..."

### **Technical Deep Dive Prompts**
1. **"Walk me through your Kubernetes implementation"**
   - Pull up GitHub repo
   - Show YAML files
   - Explain architecture decisions
   - Discuss scaling and reliability

2. **"Tell me about your GCP experience"**
   - Show live Cloud Run services
   - Discuss Vertex AI integration
   - Explain auto-scaling setup
   - Walk through cost optimization

3. **"How did you implement the RAG system?"**
   - Show architecture diagram
   - Explain vector database choice
   - Discuss embedding strategy
   - Demo the chatbot live

4. **"What's your Infrastructure as Code experience?"**
   - Show Terraform code
   - Explain resource management
   - Discuss state management
   - Demonstrate reproducibility

### **The Closer**
> "This entire portfolio - frontend, backend, RAG system, K8s deployment, 
> GCP infrastructure - I built it in 12-14 hours to prove I'm a fast learner 
> who ships working code. Imagine what I'll build in my first 90 days 
> embedded with your team. When can I start?"

---

## 📝 DOCUMENTATION STANDARDS

### **Code Documentation**
```python
# Every file should have:

"""
Module: rag_service.chatbot
Purpose: RAG-powered chatbot for portfolio queries
Author: Vasu Kapoor
Created: Nov 2, 2025

This module implements a Retrieval-Augmented Generation system
that answers questions about my AI/ML platform engineering journey.

Architecture:
- Vector Store: ChromaDB for document embeddings
- LLM: OpenAI GPT-4 for response generation
- Knowledge Base: Portfolio documentation and code

Usage:
    chatbot = RAGChatbot(vector_store)
    response = chatbot.query("How did you learn Kubernetes?")
"""
```

### **README Standards**
```markdown
# Project Name

## Overview
Brief description of what this does

## Architecture
High-level architecture diagram

## Tech Stack
- Technology 1: Purpose
- Technology 2: Purpose

## Setup
Step-by-step installation

## Usage
How to use/deploy

## Testing
How to test

## Deployment
Deployment instructions

## Contributing
N/A (personal project)

## License
MIT

## Author
Vasu Kapoor - [LinkedIn] - [Email]
```

---

## 🚀 DEPLOYMENT CHECKLIST

### **Pre-Deployment**
- [ ] All environment variables configured
- [ ] Database migrations run
- [ ] Static files collected
- [ ] API endpoints tested
- [ ] CORS configured correctly
- [ ] SSL/HTTPS setup
- [ ] Custom domain configured
- [ ] Error tracking enabled

### **Post-Deployment**
- [ ] Health checks passing
- [ ] Monitoring dashboards setup
- [ ] Logs accessible
- [ ] Auto-scaling working
- [ ] Backups configured
- [ ] Documentation updated
- [ ] GitHub repo public
- [ ] LinkedIn post published

---

## 💰 COST ESTIMATE

### **Development Phase**
```
Time Investment: 14-16 hours
Cost: $0 (your time)
```

### **Hosting Costs (Monthly)**
```
Frontend (Vercel): $0 (free tier)
Backend (GCP Cloud Run): $5-10 (free tier + minimal usage)
RAG Service (Cloud Run): $5-10
Database (Cloud SQL): $7 (db-f1-micro)
Domain (optional): $12/year
Total: ~$15-25/month

Note: Can run 100% free using:
- Frontend: Vercel/Netlify free tier
- Backend: Cloud Run free tier (2M requests/month)
- Database: Firestore free tier
- RAG: Run on same Cloud Run instance as backend
```

### **API Costs**
```
OpenAI Embeddings: ~$0.01 per 1000 queries
OpenAI GPT-4: ~$0.03 per query
Monthly (100 queries): < $5
```

**Total Monthly Cost: $20-30** (less if using free tiers)

---

## 🎯 TIMELINE SUMMARY

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| 1. Foundation | 4-5h | Basic app structure, API setup |
| 2. Content | 4-5h | Documentation, pages, visuals |
| 3. RAG Chatbot | 3-4h | Vector store, query system, widget |
| 4. Deployment | 2-3h | GCP, Vercel, IaC, CI/CD |
| 5. Polish | 2h | Performance, SEO, testing |
| **TOTAL** | **15-19h** | **Production-ready portfolio** |

---

## 🏆 EXPECTED OUTCOMES

### **Immediate Benefits**
1. **Stand Out from Candidates**
   - Only one with interactive portfolio
   - Proof of learning velocity
   - Live deployments to showcase

2. **Interview Confidence**
   - Have working code to show
   - Can screenshare live demos
   - Concrete examples for every question

3. **Negotiation Leverage**
   - Demonstrated fast learning
   - Production-ready skills
   - Portfolio speaks louder than promises

### **Long-Term Benefits**
1. **Career Trajectory**
   - Entry into platform engineering
   - Higher compensation potential
   - Relevant experience for future roles

2. **Skill Acquisition**
   - Kubernetes production experience
   - GCP cloud platform skills
   - IaC with Terraform
   - RAG system implementation

3. **Portfolio Asset**
   - Reusable for other applications
   - Reference for future projects
   - Personal brand building

---

## 🎬 GETTING STARTED

### **RIGHT NOW** (Next 30 minutes)
```bash
# 1. Create GitHub repo
git init ai-platform-portfolio
cd ai-platform-portfolio

# 2. Setup frontend
npm create vite@latest frontend -- --template react
cd frontend
npm install

# 3. Setup backend
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate
pip install django djangorestframework django-cors-headers

# 4. Create infrastructure folder
mkdir -p infrastructure/{terraform,kubernetes}

# 5. Start building!
code .
```

### **Hour 1-2: Foundation**
- Complete project setup
- Build basic frontend shell
- Setup Django API
- Test local integration

### **Hour 3-6: Content**
- Write documentation
- Build frontend pages
- Create visuals
- Add code examples

### **Hour 7-10: RAG System**
- Setup vector store
- Implement RAG logic
- Build chatbot widget
- Test queries

### **Hour 11-14: Deploy**
- Deploy to GCP
- Deploy to Vercel
- Setup CI/CD
- Final testing

### **Hour 15-16: Polish**
- Performance optimization
- SEO setup
- Final testing
- Launch!

---

## 🔥 MOTIVATIONAL CLOSING

### **The Reality Check**

**Without this portfolio:**
- You're "another candidate"
- 15% chance of interview
- Weak interview position
- "I can learn it" (everyone says this)
- Competing with better-qualified candidates

**With this portfolio:**
- You're "the fast learner with receipts"
- 70% chance of interview
- Strong interview position
- "I DID learn it - here's proof"
- Differentiated by demonstration

### **The Math**
```
Investment: 15-20 hours
Potential outcome: 30-50% salary increase
ROI: Literally life-changing

15 hours now = $20K+ more per year
That's $1,300+ per hour of work
```

### **The Mindset**

This isn't just about one job. This is about:
- **Proving to yourself** you can learn anything
- **Building confidence** through capability
- **Creating a system** for rapid skill acquisition
- **Establishing a reputation** as a fast learner who ships

**This portfolio becomes proof that you're not just talking - you're doing.**

---

## 🚀 FINAL CHECKLIST

Before you start building, make sure you have:

- [ ] Read the entire 12-hour sprint plan
- [ ] Understood the Wipro role requirements
- [ ] Cleared your calendar (need focused time)
- [ ] Setup development environment
- [ ] Created GitHub account/repo
- [ ] Created GCP account (free tier)
- [ ] Got OpenAI API key (for RAG)
- [ ] Mentally prepared to ship fast

---

## 📞 SUPPORT RESOURCES

### **Documentation**
- React: https://react.dev
- Django: https://docs.djangoproject.com
- Tailwind: https://tailwindcss.com
- GCP Cloud Run: https://cloud.google.com/run/docs
- Terraform: https://terraform.io/docs

### **AI Assistants**
- Use Claude/ChatGPT for:
  - Code generation
  - Debugging
  - Architecture decisions
  - Content writing
  - Problem-solving

### **Learning Resources**
- Kubernetes: kubernetes.io/docs
- Vector Databases: docs.trychroma.com
- RAG Systems: langchain.com/docs

---

## ⚡ LET'S GO!

**You have the plan.**
**You have the skills.**
**You have the time.**

**Now go build this and win that job.** 🚀🔥💪

---

**END OF BATTLE PLAN**

**Created by:** Claude (Anthropic)  
**For:** Vasu Kapoor  
**Date:** November 2, 2025  
**Purpose:** Build the portfolio that wins the Wipro AI/ML Platform Engineer role

**Clock starts now. Hour 1 begins. GO BUILD.** ⏱️🏗️