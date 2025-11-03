"""
Paper Scraper Microservice - FastAPI Application
"""

import logging
import time
import httpx
from datetime import datetime
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.models import (
    PaperData,
    ScrapeRequest,
    ScrapeJobResponse,
    HealthCheckResponse,
    JobStatus
)
from app.scrapers.arxiv import ArxivScraper
from app.scrapers.blog_scraper import scrape_all_blogs, scrape_specific_blog

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Track service start time
START_TIME = time.time()

# Job storage (in-memory for MVP, will use database later)
jobs_db = {}
papers_db = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    logger.info(f"Starting {settings.service_name} v{settings.service_version}")
    logger.info(f"Environment: {settings.environment}")
    yield
    logger.info("Shutting down Paper Scraper Service")


# Create FastAPI app
app = FastAPI(
    title="Paper Scraper Service",
    description="Microservice for scraping ML/AI research papers",
    version=settings.service_version,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    uptime = time.time() - START_TIME

    return HealthCheckResponse(
        service=settings.service_name,
        version=settings.service_version,
        status="healthy",
        timestamp=datetime.now(),
        uptime=uptime,
        checks={
            "arxiv_scraper": "ok",
            "memory": "ok",
            "environment": settings.environment
        }
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.service_name,
        "version": settings.service_version,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.post("/scrape", response_model=ScrapeJobResponse)
async def trigger_scrape(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks
):
    """
    Trigger paper scraping

    Args:
        request: Scrape request with source, days, max_results
        background_tasks: FastAPI background tasks

    Returns:
        Scrape job response with job_id
    """
    try:
        # Generate job ID
        job_id = f"{request.source}-{int(time.time())}"

        # Create job record
        job = ScrapeJobResponse(
            job_id=job_id,
            source=request.source,
            status=JobStatus.RUNNING,
            start_time=datetime.now()
        )
        jobs_db[job_id] = job

        # Run scraping in background
        background_tasks.add_task(
            run_scrape_job,
            job_id,
            request
        )

        logger.info(f"Created scrape job: {job_id}")
        return job

    except Exception as e:
        logger.error(f"Error creating scrape job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def send_webhook_to_django(job_id: str, source: str, papers: List[PaperData]):
    """
    Send webhook to Django backend with scraped papers

    Args:
        job_id: Job ID
        source: Source of papers (arxiv, etc.)
        papers: List of scraped papers
    """
    try:
        webhook_url = f"{settings.django_api_url}/api/webhooks/scraper-complete/"

        # Prepare webhook payload
        payload = {
            "job_id": job_id,
            "source": source,
            "papers": [
                {
                    "title": paper.title,
                    "abstract": paper.abstract,
                    "authors": paper.authors,
                    "source_id": paper.source_id,
                    "url": str(paper.url),  # Convert HttpUrl to string
                    "pdf_url": str(paper.pdf_url) if paper.pdf_url else None,
                    "published_date": paper.published_date.isoformat() if paper.published_date else None,
                    "category": paper.category,
                    "relevance_score": paper.relevance_score,
                    "tags": paper.tags,
                    "citation_count": paper.citation_count or 0
                }
                for paper in papers
            ],
            "total_papers": len(papers),
            "timestamp": datetime.now().isoformat()
        }

        # Send webhook with authentication
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                webhook_url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {settings.webhook_secret}",
                    "Content-Type": "application/json"
                }
            )

            if response.status_code in [200, 201]:
                logger.info(f"Webhook sent successfully to Django: {job_id}")
                result = response.json()
                logger.info(f"Django response: {result.get('papers_created', 0)} created, {result.get('papers_updated', 0)} updated")
            else:
                logger.warning(f"Webhook failed with status {response.status_code}: {response.text}")

    except Exception as e:
        # Don't fail the job if webhook fails
        logger.error(f"Error sending webhook to Django: {str(e)}")


async def run_scrape_job(job_id: str, request: ScrapeRequest):
    """
    Run scraping job in background

    Args:
        job_id: Job ID
        request: Scrape request
    """
    try:
        logger.info(f"Starting scrape job {job_id}: source={request.source}")

        papers: List[PaperData] = []

        # Scrape based on source
        if request.source == "blogs":
            # Scrape AI company blogs
            blog_posts = await scrape_all_blogs(max_per_source=request.max_results or 10)
            # Convert blog posts to PaperData format
            for idx, post in enumerate(blog_posts):
                # Map blog categories to PaperData categories
                category_map = {
                    'model-release': 'llm',
                    'research': 'nlp',
                    'products': 'mlops',
                    'models': 'multimodal'
                }
                category = category_map.get(post['category'], 'llm')

                # Generate source_id from URL
                source_id = f"{post['source']}-{hash(post['url']) % 1000000}"

                # Map source to SourceType
                source_type_map = {
                    'openai': 'arxiv',  # Using arxiv as fallback since blogs not in enum
                    'google-ai': 'arxiv',
                    'microsoft-ai': 'arxiv',
                    'huggingface': 'huggingface'
                }
                source_type = source_type_map.get(post['source'], 'arxiv')

                papers.append(PaperData(
                    title=post['title'],
                    abstract=post['abstract'],
                    authors=post['authors'],
                    source=source_type,
                    source_id=source_id,
                    url=post['url'],
                    pdf_url=None,
                    published_date=datetime.fromisoformat(post['published_date']).date(),
                    category=category,
                    relevance_score=post['relevance_score'],
                    tags=post['tags'],
                    citation_count=0
                ))
            logger.info(f"Blog scraper found {len(blog_posts)} posts")

        elif request.source in ["arxiv", "all"]:
            scraper = ArxivScraper(settings.arxiv_base_url)
            arxiv_papers = await scraper.scrape(
                days=request.days,
                max_results=request.max_results,
                category_filter=request.category
            )
            papers.extend(arxiv_papers)
            logger.info(f"arXiv scraper found {len(arxiv_papers)} papers")

        # Store papers (in-memory for now)
        papers_db.extend(papers)

        # Update job status
        job = jobs_db[job_id]
        job.status = JobStatus.COMPLETED
        job.end_time = datetime.now()
        job.papers_found = len(papers)
        job.papers_added = len(papers)

        logger.info(f"Scrape job {job_id} completed: {len(papers)} papers found")

        # Send webhook to Django backend
        await send_webhook_to_django(job_id, request.source, papers)

    except Exception as e:
        logger.error(f"Scrape job {job_id} failed: {str(e)}")
        job = jobs_db.get(job_id)
        if job:
            job.status = JobStatus.FAILED
            job.end_time = datetime.now()
            job.errors = str(e)


@app.get("/scrape/status/{job_id}", response_model=ScrapeJobResponse)
async def get_job_status(job_id: str):
    """Get scrape job status"""
    job = jobs_db.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return job


@app.get("/scrape/history")
async def get_job_history(limit: int = 10):
    """Get scrape job history"""
    jobs = list(jobs_db.values())
    jobs.sort(key=lambda x: x.start_time, reverse=True)
    return jobs[:limit]


@app.get("/papers", response_model=List[PaperData])
async def get_papers(limit: int = 20, category: str = None):
    """
    Get scraped papers (from in-memory storage)

    Args:
        limit: Max number of papers to return
        category: Filter by category

    Returns:
        List of papers
    """
    papers = papers_db

    if category:
        papers = [p for p in papers if p.category == category]

    # Sort by published date (newest first)
    papers = sorted(papers, key=lambda x: x.published_date, reverse=True)

    return papers[:limit]


@app.get("/stats")
async def get_stats():
    """Get scraper statistics"""
    completed_jobs = [j for j in jobs_db.values() if j.status == JobStatus.COMPLETED]
    failed_jobs = [j for j in jobs_db.values() if j.status == JobStatus.FAILED]

    return {
        "total_jobs": len(jobs_db),
        "completed_jobs": len(completed_jobs),
        "failed_jobs": len(failed_jobs),
        "total_papers": len(papers_db),
        "papers_by_category": {
            "llm": len([p for p in papers_db if p.category == "llm"]),
            "cv": len([p for p in papers_db if p.category == "cv"]),
            "rag": len([p for p in papers_db if p.category == "rag"]),
            "mlops": len([p for p in papers_db if p.category == "mlops"]),
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.environment == "development"
    )
