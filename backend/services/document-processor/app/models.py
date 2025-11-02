# Document Processor Service - Data Models
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ProcessingStatus(str, Enum):
    """Processing job status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentType(str, Enum):
    """Document type"""
    PDF = "pdf"
    TEXT = "text"
    GITHUB = "github"
    MARKDOWN = "markdown"


class ProcessPDFRequest(BaseModel):
    """Request to process a PDF document"""
    url: HttpUrl
    title: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ProcessTextRequest(BaseModel):
    """Request to process raw text"""
    text: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    metadata: Optional[Dict[str, Any]] = None


class ProcessGitHubRequest(BaseModel):
    """Request to process a GitHub repository"""
    repo_url: HttpUrl
    branch: str = "main"
    include_patterns: Optional[List[str]] = ["*.md", "*.py", "*.js", "*.ts"]
    exclude_patterns: Optional[List[str]] = ["node_modules/**", "venv/**", ".git/**"]


class ProcessingJob(BaseModel):
    """Processing job details"""
    job_id: str
    document_type: DocumentType
    status: ProcessingStatus
    created_at: datetime
    updated_at: datetime
    chunks_processed: int = 0
    total_chunks: int = 0
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ProcessingResponse(BaseModel):
    """Response after initiating processing"""
    job_id: str
    status: ProcessingStatus
    message: str
    estimated_time_seconds: Optional[int] = None


class ChunkData(BaseModel):
    """Processed text chunk"""
    chunk_id: str
    text: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    service: str
    version: str
    status: str
    timestamp: datetime
    uptime: float
    checks: Dict[str, str]


class JobStatusResponse(BaseModel):
    """Job status response"""
    job_id: str
    status: ProcessingStatus
    progress: float  # 0-100
    chunks_processed: int
    total_chunks: int
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None
