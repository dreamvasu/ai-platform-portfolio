# RAG Chatbot Setup Guide (Google Vertex AI)

## 🎯 Why Vertex AI?

This RAG system uses **Google Vertex AI** to demonstrate hands-on **GCP AI Platform** experience:
- ✅ Vertex AI Text Embeddings (textembedding-gecko@003)
- ✅ Vertex AI Gemini Pro (generative AI)
- ✅ Shows GCP cloud expertise for the Wipro role

## 🚀 Quick Start

### 1. Set up Google Cloud Platform

**A. Create GCP Project**
```bash
# Install gcloud CLI if you haven't
# https://cloud.google.com/sdk/docs/install

# Login to GCP
gcloud auth login

# Create a new project
gcloud projects create your-portfolio-project --name="AI Portfolio"

# Set as default project
gcloud config set project your-portfolio-project

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage-component.googleapis.com
```

**B. Set up Authentication**
```bash
# Create service account
gcloud iam service-accounts create portfolio-rag \
    --display-name="Portfolio RAG Service"

# Grant necessary roles
gcloud projects add-iam-policy-binding your-portfolio-project \
    --member="serviceAccount:portfolio-rag@your-portfolio-project.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Create and download key
gcloud iam service-accounts keys create ~/portfolio-key.json \
    --iam-account=portfolio-rag@your-portfolio-project.iam.gserviceaccount.com
```

**C. Set Environment Variables**
```bash
# In backend directory
export GOOGLE_CLOUD_PROJECT='your-portfolio-project'
export GOOGLE_APPLICATION_CREDENTIALS=~/portfolio-key.json
```

Or create a `.env` file:
```bash
cp .env.example .env
# Then edit .env and add:
# GOOGLE_CLOUD_PROJECT=your-portfolio-project
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/portfolio-key.json
```

### 2. Ingest Documentation

This loads all markdown docs into the vector database:

```bash
cd backend
source venv/bin/activate
python ingest_documents.py
```

This will:
- Load markdown files from `docs/planning/`, root directory, etc.
- Chunk them into ~500 word pieces
- Generate embeddings using OpenAI
- Store in ChromaDB vector database
- Create `./chroma_db/` directory with the data

Expected output:
```
🚀 STARTING DOCUMENT INGESTION FOR RAG SYSTEM
📦 Initializing components...
📚 Loading markdown documents...
  📄 Loaded: architecture.md
  📄 Loaded: backend-rag.md
  ...
✅ Loaded 9 markdown files
✂️  Processing documents into chunks...
✅ Created 47 chunks from 9 documents
🧮 Generating embeddings for 47 chunks...
✅ Generated 47 embeddings
💾 Adding to vector store...
✅ Added 47 documents to vector store
🎉 DOCUMENT INGESTION COMPLETE!
```

### 3. Start Django Server

```bash
python manage.py runserver
```

### 4. Test Chatbot API

**Health Check:**
```bash
curl http://127.0.0.1:8000/api/chatbot/health/
```

**Query Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/chatbot/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "How did Vasu learn Kubernetes?"}'
```

**Suggested Questions:**
```bash
curl http://127.0.0.1:8000/api/chatbot/suggestions/
```

### 5. Test Frontend Widget

1. Make sure frontend is running: `cd frontend && npm run dev`
2. Open http://localhost:5173
3. Click the "🤖 Ask AI Assistant" button in bottom-right
4. Ask a question!

---

## 📊 API Endpoints

### POST `/api/chatbot/query/`
Ask a question to the RAG chatbot

**Request:**
```json
{
  "question": "How did Vasu learn Kubernetes?",
  "k": 5,
  "include_sources": true
}
```

**Response:**
```json
{
  "answer": "Vasu learned Kubernetes during...",
  "context_used": 5,
  "sources": [
    {
      "source": "docs/planning/architecture.md",
      "category": "planning",
      "chunk_id": 3,
      "relevance_score": 0.85
    }
  ]
}
```

### GET `/api/chatbot/suggestions/`
Get suggested questions

**Response:**
```json
{
  "questions": [
    "How did Vasu learn Kubernetes?",
    "What's Vasu's experience with GCP?",
    ...
  ]
}
```

### GET `/api/chatbot/health/`
Check chatbot health

**Response:**
```json
{
  "status": "healthy",
  "vector_store_documents": 47,
  "ready": true
}
```

---

## 🔧 Troubleshooting

**Error: "OPENAI_API_KEY environment variable not set"**
- Set the API key: `export OPENAI_API_KEY='your-key'`

**Error: "No documents found to ingest"**
- Check that docs exist in `docs/planning/`, `CLAUDE.md`, etc.
- Run from backend directory

**Error: "I don't have enough information"**
- Run `python ingest_documents.py` to populate vector store
- Check health endpoint to see if docs are loaded

**Frontend can't connect to chatbot**
- Make sure Django server is running on port 8000
- Check browser console for CORS errors
- Verify CORS settings in `core/settings.py`

---

## 📁 Project Structure

```
backend/
├── rag_service/
│   ├── vector_store.py      # ChromaDB wrapper
│   ├── embeddings.py         # OpenAI embeddings
│   ├── document_processor.py # Text chunking
│   ├── chatbot.py            # RAG logic
│   ├── views.py              # API endpoints
│   ├── serializers.py        # Request/response schemas
│   └── urls.py               # URL routing
├── chroma_db/               # Vector database (created after ingestion)
├── ingest_documents.py      # Ingestion script
└── RAG_SETUP.md            # This file
```

---

## 🎯 Next Steps

After getting the RAG system working:

1. **Add More Documentation**
   - Create technical deep-dive docs about:
     - RAG system architecture
     - ChromaDB implementation
     - OpenAI integration
     - Django REST Framework setup
     - React architecture
   - Re-run `python ingest_documents.py` to update vector store

2. **Improve Chatbot**
   - Tune chunk size and overlap
   - Experiment with different embedding models
   - Add conversation history
   - Implement streaming responses

3. **Deploy to GCP**
   - Dockerize the RAG service
   - Deploy to Cloud Run
   - Use Cloud Storage for vector DB persistence
   - Set environment variables in GCP

---

## 💡 Tips

- **Cost**: OpenAI embeddings are ~$0.01 per 1000 chunks. GPT-4 queries are ~$0.03 each.
- **Speed**: First query after server start takes longer (loading models)
- **Quality**: More detailed documentation = better answers
- **Context**: The chatbot uses top-5 most relevant chunks by default
