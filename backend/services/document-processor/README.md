# Document Processor Microservice

FastAPI-based microservice for processing documents (PDFs, text, GitHub repos) and storing them in a vector database for RAG (Retrieval Augmented Generation).

## Features

- 🚀 Async document processing with FastAPI
- 📄 PDF text extraction (PyPDF2 + pdfplumber fallback)
- 📊 ChromaDB vector storage for embeddings
- 🔍 Intelligent text chunking with overlap
- 📈 Background job processing
- 🎯 Query endpoints for RAG
- 🐳 Docker support for Cloud Run

## Tech Stack

- **Framework:** FastAPI 0.104.1
- **Server:** Uvicorn (ASGI)
- **PDF Processing:** PyPDF2 3.0.1, pdfplumber 0.10.3
- **Vector DB:** ChromaDB 0.4.18
- **Cloud:** Google Cloud Storage, Vertex AI
- **Text Processing:** LangChain 0.1.0

## Quick Start

### Local Development

1. **Setup environment:**
```bash
cd services/document-processor

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

2. **Run the service:**
```bash
# Development mode (auto-reload)
uvicorn app.main:app --reload --port 8003

# Or use Python directly
python -m app.main
```

3. **Access the service:**
- API: http://localhost:8003
- Docs: http://localhost:8003/docs
- Health: http://localhost:8003/health

## API Endpoints

### Health Check
```http
GET /health
```

Response:
```json
{
  "service": "document-processor",
  "version": "1.0.0",
  "status": "healthy",
  "timestamp": "2025-11-03T12:00:00",
  "uptime": 123.45,
  "checks": {
    "vector_store": "ok",
    "pdf_processor": "ok"
  }
}
```

### Process PDF
```http
POST /process/pdf
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "title": "My Document",
  "metadata": {
    "author": "John Doe",
    "category": "research"
  }
}
```

Response:
```json
{
  "job_id": "pdf-1699000000",
  "status": "pending",
  "message": "PDF processing started",
  "estimated_time_seconds": 30
}
```

### Process Text
```http
POST /process/text
Content-Type: application/json

{
  "text": "Your long document text here...",
  "title": "Document Title",
  "metadata": {
    "source": "manual_input"
  }
}
```

### Get Job Status
```http
GET /jobs/{job_id}
```

Response:
```json
{
  "job_id": "pdf-1699000000",
  "status": "completed",
  "progress": 100.0,
  "chunks_processed": 15,
  "total_chunks": 15,
  "created_at": "2025-11-03T12:00:00",
  "updated_at": "2025-11-03T12:00:30",
  "error_message": null
}
```

### List Jobs
```http
GET /jobs?limit=10&status=completed
```

### Query Documents
```http
GET /query?q=kubernetes deployment&k=5
```

Response:
```json
{
  "query": "kubernetes deployment",
  "results": [
    {
      "id": "chunk_0",
      "text": "Relevant document chunk...",
      "metadata": {
        "title": "K8s Guide",
        "chunk_index": 0
      },
      "distance": 0.85
    }
  ],
  "count": 5
}
```

### Get Statistics
```http
GET /stats
```

Response:
```json
{
  "vector_store": {
    "total_documents": 150
  },
  "jobs": {
    "total": 10,
    "pending": 0,
    "processing": 1,
    "completed": 8,
    "failed": 1
  }
}
```

## Configuration

Environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVICE_NAME` | document-processor | Service name |
| `SERVICE_VERSION` | 1.0.0 | Service version |
| `ENVIRONMENT` | development | Environment |
| `PORT` | 8003 | Server port |
| `DJANGO_API_URL` | http://localhost:8000 | Django backend URL |
| `CHROMADB_PERSIST_DIRECTORY` | ./chromadb_data | ChromaDB data directory |
| `CHUNK_SIZE` | 1000 | Text chunk size (characters) |
| `CHUNK_OVERLAP` | 200 | Chunk overlap (characters) |

## Document Processing

### PDF Processing Flow

1. **Download**: PDF downloaded from URL via httpx
2. **Extract**: Text extracted using PyPDF2 (fallback to pdfplumber)
3. **Chunk**: Text split into chunks with overlap
4. **Embed**: Chunks embedded using ChromaDB default embeddings
5. **Store**: Chunks stored in ChromaDB vector database

### Text Chunking

- **Chunk Size**: 1000 characters (configurable)
- **Overlap**: 200 characters (configurable)
- **Smart Breaks**: Prefers paragraph/sentence boundaries
- **Metadata**: Each chunk includes position, size, and custom metadata

## Deployment

### Google Cloud Run

1. **Build and deploy:**
```bash
gcloud run deploy document-processor \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production \
  --port 8003 \
  --memory 1Gi \
  --timeout 300
```

2. **With Cloud Storage:**
```bash
gcloud run deploy document-processor \
  --source . \
  --region us-central1 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=your-project,GOOGLE_CLOUD_BUCKET=your-bucket
```

### Docker

```bash
# Build image
docker build -t document-processor:latest .

# Run locally
docker run -p 8003:8003 \
  -v $(pwd)/chromadb_data:/app/chromadb_data \
  document-processor:latest
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: document-processor
spec:
  replicas: 2
  selector:
    matchLabels:
      app: document-processor
  template:
    metadata:
      labels:
        app: document-processor
    spec:
      containers:
      - name: document-processor
        image: document-processor:latest
        ports:
        - containerPort: 8003
        env:
        - name: ENVIRONMENT
          value: "production"
        volumeMounts:
        - name: chromadb-storage
          mountPath: /app/chromadb_data
      volumes:
      - name: chromadb-storage
        persistentVolumeClaim:
          claimName: chromadb-pvc
```

## Project Structure

```
document-processor/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── models.py            # Pydantic models
│   └── processors/
│       ├── __init__.py
│       ├── pdf_processor.py  # PDF processing
│       └── vector_store.py   # ChromaDB integration
├── chromadb_data/           # ChromaDB persistent storage
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## ChromaDB

### Data Structure

- **Collection Name**: `portfolio_documents`
- **Embedding Model**: ChromaDB default (sentence-transformers)
- **Metadata Fields**:
  - `title`: Document title
  - `document_type`: pdf, text, github
  - `chunk_index`: Chunk position
  - `chunk_size`: Chunk length
  - Custom metadata from requests

### Persistence

ChromaDB data is persisted to `./chromadb_data` directory. Mount this as a volume in production for data persistence.

## Testing

### Manual Testing

```bash
# Health check
curl http://localhost:8003/health

# Process PDF
curl -X POST http://localhost:8003/process/pdf \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com/doc.pdf", "title": "Test Doc"}'

# Check job status
curl http://localhost:8003/jobs/pdf-1699000000

# Query documents
curl "http://localhost:8003/query?q=kubernetes&k=5"
```

## Troubleshooting

**Issue:** ChromaDB not initializing
- Check `CHROMADB_PERSIST_DIRECTORY` exists and is writable
- Verify ChromaDB dependencies installed
- Review logs for specific error messages

**Issue:** PDF processing fails
- Verify PDF URL is accessible
- Check PDF is not password-protected
- Try with pdfplumber fallback

**Issue:** Out of memory
- Reduce `CHUNK_SIZE`
- Increase Cloud Run memory allocation
- Process smaller documents or use pagination

## Future Enhancements

- [ ] GitHub repository processing
- [ ] Vertex AI embeddings integration
- [ ] Celery for distributed processing
- [ ] Redis for job queue
- [ ] Webhook notifications
- [ ] Batch processing
- [ ] Document deduplication
- [ ] Advanced metadata extraction

## License

Part of AI/ML Platform Engineer Portfolio

---

**Built with FastAPI & ChromaDB** | **Deployed on Cloud Run** | **Vasu Kapoor 2025**
