"""
Pydantic models for Paper Scraper Service
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal
from datetime import datetime, date
from enum import Enum


class SourceType(str, Enum):
    """Source types for papers"""
    ARXIV = "arxiv"
    HUGGINGFACE = "huggingface"
    PAPERSWITHCODE = "paperswithcode"
    SCHOLAR = "scholar"


class CategoryType(str, Enum):
    """Paper categories"""
    LLM = "llm"
    CV = "cv"
    RAG = "rag"
    MLOPS = "mlops"
    TRAINING = "training"
    INFERENCE = "inference"
    NLP = "nlp"
    MULTIMODAL = "multimodal"


class JobStatus(str, Enum):
    """Scraper job status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class PaperData(BaseModel):
    """Paper data model"""
    title: str = Field(..., min_length=1, max_length=500)
    abstract: str = Field(..., min_length=1)
    authors: str = Field(..., description="Comma-separated list of authors")
    source: SourceType
    source_id: str = Field(..., description="Unique ID from source")
    url: HttpUrl
    pdf_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    published_date: date
    category: CategoryType
    tags: List[str] = Field(default_factory=list)
    relevance_score: float = Field(default=0.5, ge=0.0, le=1.0)
    citation_count: int = Field(default=0, ge=0)


class ScrapeRequest(BaseModel):
    """Request model for scraping"""
    source: Literal["arxiv", "huggingface", "paperswithcode", "blogs", "all"] = "arxiv"
    days: int = Field(default=7, ge=1, le=365, description="Look back N days")
    max_results: int = Field(default=50, ge=1, le=500)
    category: Optional[CategoryType] = None


class ScrapeJobResponse(BaseModel):
    """Response model for scrape job"""
    job_id: str
    source: str
    status: JobStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    papers_found: int = 0
    papers_added: int = 0
    errors: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    service: str
    version: str
    status: Literal["healthy", "unhealthy"]
    timestamp: datetime
    uptime: float
    checks: dict


class ScraperStatsResponse(BaseModel):
    """Scraper statistics"""
    total_jobs: int
    successful_jobs: int
    failed_jobs: int
    total_papers_scraped: int
    last_run: Optional[datetime] = None
