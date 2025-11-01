# GCP Vertex AI Implementation - Proof of Hands-On Experience

## 🎯 Why This Matters for Wipro Role

The Wipro AI/ML Platform Engineer role specifically states:
> "Strong understanding of private and public cloud technologies... **GCP experience preferred**"

This implementation demonstrates **hands-on Google Cloud Platform AI expertise** by using:

## ✅ GCP Services Used

### 1. **Vertex AI Text Embeddings** (textembedding-gecko@003)
- **Purpose:** Convert text documents into vector embeddings for semantic search
- **Implementation:** `rag_service/embeddings.py`
- **API Used:** `vertexai.language_models.TextEmbeddingModel`
- **Features:**
  - Batch processing (up to 250 texts per request)
  - 768-dimensional embeddings
  - Optimized for semantic search

### 2. **Vertex AI Gemini Pro** (gemini-pro)
- **Purpose:** Generate intelligent responses using RAG (Retrieval-Augmented Generation)
- **Implementation:** `rag_service/chatbot.py`
- **API Used:** `vertexai.generative_models.GenerativeModel`
- **Features:**
  - Context-aware text generation
  - Temperature and token control
  - Grounded responses based on retrieved documents

### 3. **ChromaDB Vector Store**
- **Purpose:** Store and retrieve document embeddings
- **Implementation:** `rag_service/vector_store.py`
- **Integration:** Works seamlessly with Vertex AI embeddings
- **Features:**
  - Persistent storage
  - Similarity search with distance metrics
  - Metadata filtering

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER QUERY                                │
│               "How did Vasu learn K8s?"                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              DJANGO REST API                                 │
│          /api/chatbot/query/                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              RAG CHATBOT (chatbot.py)                        │
│                                                              │
│  1. Generate query embedding                                │
│     └─> Vertex AI Text Embeddings API                       │
│                                                              │
│  2. Search ChromaDB                                          │
│     └─> Find top 5 relevant documents                        │
│                                                              │
│  3. Build context from retrieved docs                        │
│                                                              │
│  4. Generate answer                                          │
│     └─> Vertex AI Gemini Pro API                            │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              RESPONSE WITH SOURCES                           │
│    {                                                         │
│      "answer": "Vasu learned Kubernetes...",                │
│      "sources": [...],                                       │
│      "context_used": 5                                       │
│    }                                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Technical Implementation Details

### Code Structure

```
backend/rag_service/
├── embeddings.py          # Vertex AI Text Embeddings
├── chatbot.py             # Vertex AI Gemini Pro + RAG logic
├── vector_store.py        # ChromaDB wrapper
├── document_processor.py  # Text chunking
├── views.py               # Django REST API endpoints
├── serializers.py         # API schemas
└── urls.py                # URL routing
```

### Key Code Snippets

**Vertex AI Embeddings Initialization:**
```python
from vertexai.language_models import TextEmbeddingModel
import vertexai

vertexai.init(project=project_id, location="us-central1")
model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
```

**Gemini Pro Response Generation:**
```python
from vertexai.generative_models import GenerativeModel

model = GenerativeModel("gemini-pro")
response = model.generate_content(
    prompt,
    generation_config={
        "temperature": 0.7,
        "max_output_tokens": 500,
    }
)
```

---

## 🚀 How to Run

### Prerequisites
1. GCP Account with billing enabled
2. Vertex AI API enabled
3. Service account with `roles/aiplatform.user` role
4. Service account key JSON file

### Setup Steps

```bash
# 1. Set environment variables
export GOOGLE_CLOUD_PROJECT='your-project-id'
export GOOGLE_APPLICATION_CREDENTIALS='/path/to/key.json'

# 2. Ingest documentation
python ingest_documents.py

# 3. Start Django server
python manage.py runserver

# 4. Test chatbot API
curl -X POST http://127.0.0.1:8000/api/chatbot/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "How did Vasu learn GCP?"}'
```

---

## 📈 Performance Metrics

### Embeddings
- **Model:** textembedding-gecko@003
- **Dimensions:** 768
- **Batch Size:** 250 texts/request
- **Latency:** ~100-200ms per batch

### Generation
- **Model:** gemini-pro
- **Max Tokens:** 500
- **Temperature:** 0.7
- **Latency:** ~1-3 seconds per query

### Cost Estimate
- **Embeddings:** ~$0.00002 per 1000 characters
- **Generation:** ~$0.00025 per 1000 characters (input)
- **Total for 100 queries:** < $0.50

---

## 🎓 What This Demonstrates

### For the Wipro Interview:

**1. GCP AI Platform Hands-On Experience**
- "I implemented a production RAG system using Vertex AI"
- "I integrated both Text Embeddings and Gemini Pro models"
- "I understand GCP IAM, service accounts, and API authentication"

**2. Modern AI Architecture**
- "I built a Retrieval-Augmented Generation system"
- "I understand semantic search with vector embeddings"
- "I can architect AI systems that ground LLM responses in real data"

**3. Production-Ready Code**
- "I wrote clean, documented Python code"
- "I implemented proper error handling and batch processing"
- "I built RESTful APIs with Django REST Framework"

**4. Fast Learning**
- "I went from zero Vertex AI experience to working implementation in hours"
- "I documented everything for reproducibility"
- "I can quickly learn new cloud services and APIs"

---

## 💡 Interview Talking Points

### Question: "Do you have GCP experience?"

> "Yes, I have hands-on GCP experience with Vertex AI. I built a production RAG system using Vertex AI Text Embeddings for semantic search and Gemini Pro for response generation.
>
> The system processes documentation, generates vector embeddings, stores them in ChromaDB, and retrieves relevant context to answer questions. It's deployed as a Django REST API and powers the chatbot on my portfolio site.
>
> I understand GCP IAM, service accounts, API authentication, and the Vertex AI SDK. I can show you the live implementation and walk through the code if you'd like."

### Question: "How did you learn Vertex AI?"

> "When I saw the Wipro role preferred GCP, I dedicated time to learning Vertex AI specifically. I read the documentation, experimented with the APIs, and built a working RAG system.
>
> The concepts transferred from my Azure OpenAI experience - both are managed AI platforms with embedding and LLM services. The main difference is GCP's IAM model and the Vertex AI SDK, which I picked up quickly.
>
> I believe in learning by building. Theory only goes so far - I needed working code to truly understand the platform."

---

## 🔗 Related Documentation

- See `RAG_SETUP.md` for full setup instructions
- See `../docs/planning/backend-rag.md` for architecture details
- See code in `rag_service/` for implementation

---

**This implementation proves hands-on GCP AI Platform experience, not just theoretical knowledge. It's working code that can be deployed, tested, and demonstrated in interviews.** 🚀
