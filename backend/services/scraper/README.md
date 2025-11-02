# Paper Scraper Microservice

FastAPI-based microservice for scraping ML/AI research papers from multiple sources.

## Features

- 🚀 Async scraping with FastAPI
- 📄 arXiv API integration (tested and working)
- 🎯 Intelligent paper categorization (LLM, RAG, MLOps, CV, etc.)
- 📊 Relevance scoring
- 🏷️ Automatic tag extraction
- 🔍 Background job processing
- 📈 Health checks and metrics
- 🐳 Docker support for Cloud Run

## Tech Stack

- **Framework:** FastAPI 0.104.1
- **Server:** Uvicorn (ASGI)
- **Validation:** Pydantic v2
- **HTTP Client:** httpx (async)
- **Parsing:** BeautifulSoup4, feedparser

## Quick Start

### Local Development

1. **Setup environment:**
```bash
cd services/scraper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

2. **Run the service:**
```bash
# Development mode (auto-reload)
uvicorn app.main:app --reload --port 8001

# Or use Python directly
python -m app.main
```

3. **Access the service:**
- API: http://localhost:8001
- Docs: http://localhost:8001/docs
- Health: http://localhost:8001/health

### Docker

```bash
# Build image
docker build -t paper-scraper:latest .

# Run container
docker run -p 8001:8001 paper-scraper:latest

# With environment variables
docker run -p 8001:8001 \
  -e DJANGO_API_URL=http://host.docker.internal:8000 \
  paper-scraper:latest
```

## API Endpoints

### Health Check
```http
GET /health
```

Response:
```json
{
  "service": "paper-scraper",
  "version": "1.0.0",
  "status": "healthy",
  "timestamp": "2025-11-03T02:00:00",
  "uptime": 123.45,
  "checks": {
    "arxiv_scraper": "ok",
    "memory": "ok"
  }
}
```

### Trigger Scraping
```http
POST /scrape
Content-Type: application/json

{
  "source": "arxiv",
  "days": 7,
  "max_results": 50,
  "category": "llm"
}
```

Response:
```json
{
  "job_id": "arxiv-1699000000",
  "source": "arxiv",
  "status": "running",
  "start_time": "2025-11-03T02:00:00",
  "papers_found": 0
}
```

### Job Status
```http
GET /scrape/status/{job_id}
```

### Job History
```http
GET /scrape/history?limit=10
```

### Get Papers
```http
GET /papers?limit=20&category=llm
```

### Statistics
```http
GET /stats
```

## Configuration

Environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVICE_NAME` | paper-scraper | Service name |
| `SERVICE_VERSION` | 1.0.0 | Service version |
| `ENVIRONMENT` | development | Environment (development/production) |
| `PORT` | 8001 | Server port |
| `DJANGO_API_URL` | http://localhost:8000 | Django backend URL |
| `LOG_LEVEL` | INFO | Logging level |
| `MAX_RESULTS_PER_SOURCE` | 100 | Max papers per source |

## Deployment

### Google Cloud Run

1. **Build and push to Artifact Registry:**
```bash
# Set variables
PROJECT_ID=your-project-id
REGION=us-central1
SERVICE_NAME=paper-scraper

# Build and push
gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/portfolio/${SERVICE_NAME}
```

2. **Deploy to Cloud Run:**
```bash
gcloud run deploy ${SERVICE_NAME} \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/portfolio/${SERVICE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production,DJANGO_API_URL=https://backend.vasukapoor.com \
  --port 8001
```

3. **Setup Cloud Scheduler (daily scraping):**
```bash
gcloud scheduler jobs create http scraper-daily \
  --location ${REGION} \
  --schedule "0 2 * * *" \
  --uri "https://paper-scraper-xxxxx.run.app/scrape" \
  --http-method POST \
  --message-body '{"source":"arxiv","days":1,"max_results":50}'
```

## Development

### Project Structure
```
scraper/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── models.py            # Pydantic models
│   └── scrapers/
│       ├── __init__.py
│       ├── arxiv.py         # arXiv scraper
│       ├── huggingface.py   # HuggingFace (future)
│       └── paperswithcode.py # Papers with Code (future)
├── tests/
│   └── test_arxiv.py
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

### Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=app tests/

# Test specific scraper
python -c "
import asyncio
from app.scrapers.arxiv import ArxivScraper

async def test():
    scraper = ArxivScraper()
    papers = await scraper.scrape(days=7, max_results=10)
    print(f'Found {len(papers)} papers')

asyncio.run(test())
"
```

### Adding New Scrapers

1. Create scraper class in `app/scrapers/new_scraper.py`
2. Implement `scrape()` method returning `List[PaperData]`
3. Add to `main.py` scraping logic
4. Update tests

## Monitoring

- **Health Check:** `/health` endpoint
- **Logs:** Structured JSON logging
- **Metrics:** `/stats` endpoint with job and paper counts

## Troubleshooting

**Issue:** Papers not being scraped
- Check `/health` endpoint
- Verify arXiv API is accessible
- Check logs for errors

**Issue:** Service not starting
- Verify Python version (3.11+)
- Check all dependencies installed
- Review environment variables

**Issue:** Memory errors
- Reduce `max_results` parameter
- Implement pagination
- Add memory limits in Docker/Cloud Run

## Future Enhancements

- [ ] HuggingFace scraper
- [ ] Papers with Code scraper
- [ ] Redis for job storage
- [ ] Webhook notifications to Django
- [ ] Rate limiting
- [ ] Prometheus metrics
- [ ] Retry logic with exponential backoff

## License

Part of AI/ML Platform Engineer Portfolio

---

**Built with FastAPI** | **Deployed on Cloud Run** | **Vasu Kapoor 2025**
