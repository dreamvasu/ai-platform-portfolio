# Document Processor Service - Main Application
import time
import logging
import asyncio
from datetime import datetime
from typing import Dict
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models import (
    ProcessPDFRequest,
    ProcessTextRequest,
    ProcessingResponse,
    JobStatusResponse,
    HealthCheckResponse,
    ProcessingStatus,
    DocumentType,
)
from app.processors import PDFProcessor, vector_store

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Document Processor Service",
    description="Process documents and store in vector database for RAG",
    version=settings.service_version,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin] if settings.cors_origin != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
pdf_processor = PDFProcessor(
    chunk_size=settings.chunk_size,
    chunk_overlap=settings.chunk_overlap,
)

# In-memory job storage (in production, use Redis or database)
jobs: Dict[str, Dict] = {}

# Startup time
startup_time = time.time()


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"Starting {settings.service_name} v{settings.service_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Vector store documents: {vector_store.count()}")


@app.get("/", tags=["General"])
async def root():
    """Root endpoint with service info"""
    return {
        "service": settings.service_name,
        "version": settings.service_version,
        "environment": settings.environment,
        "endpoints": {
            "health": "GET /health",
            "process_pdf": "POST /process/pdf",
            "process_text": "POST /process/text",
            "job_status": "GET /jobs/{job_id}",
            "jobs_list": "GET /jobs",
            "query": "GET /query",
        },
    }


@app.get("/health", response_model=HealthCheckResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    uptime = time.time() - startup_time

    checks = {
        "vector_store": "ok" if vector_store.collection else "not_initialized",
        "pdf_processor": "ok",
    }

    return HealthCheckResponse(
        service=settings.service_name,
        version=settings.service_version,
        status="healthy",
        timestamp=datetime.now(),
        uptime=uptime,
        checks=checks,
    )


async def process_pdf_task(job_id: str, request: ProcessPDFRequest):
    """Background task to process PDF"""
    try:
        # Update job status
        jobs[job_id]["status"] = ProcessingStatus.PROCESSING
        jobs[job_id]["updated_at"] = datetime.now()

        logger.info(f"Processing PDF for job {job_id}: {request.url}")

        # Process PDF
        metadata = request.metadata or {}
        metadata["title"] = request.title or str(request.url)
        metadata["document_type"] = DocumentType.PDF
        metadata["job_id"] = job_id

        chunks = await pdf_processor.process_pdf(str(request.url), metadata)

        # Store in vector database
        docs_added = vector_store.add_documents(chunks)

        # Update job
        jobs[job_id]["status"] = ProcessingStatus.COMPLETED
        jobs[job_id]["chunks_processed"] = len(chunks)
        jobs[job_id]["total_chunks"] = len(chunks)
        jobs[job_id]["updated_at"] = datetime.now()

        logger.info(f"Job {job_id} completed: {docs_added} documents added")

    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        jobs[job_id]["status"] = ProcessingStatus.FAILED
        jobs[job_id]["error_message"] = str(e)
        jobs[job_id]["updated_at"] = datetime.now()


@app.post("/process/pdf", response_model=ProcessingResponse, tags=["Processing"])
async def process_pdf(request: ProcessPDFRequest, background_tasks: BackgroundTasks):
    """Process a PDF document"""
    # Create job
    job_id = f"pdf-{int(time.time())}"

    jobs[job_id] = {
        "job_id": job_id,
        "document_type": DocumentType.PDF,
        "status": ProcessingStatus.PENDING,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "chunks_processed": 0,
        "total_chunks": 0,
        "error_message": None,
        "metadata": {
            "url": str(request.url),
            "title": request.title,
        },
    }

    # Start background processing
    background_tasks.add_task(process_pdf_task, job_id, request)

    return ProcessingResponse(
        job_id=job_id,
        status=ProcessingStatus.PENDING,
        message="PDF processing started",
        estimated_time_seconds=30,
    )


async def process_text_task(job_id: str, request: ProcessTextRequest):
    """Background task to process text"""
    try:
        # Update job status
        jobs[job_id]["status"] = ProcessingStatus.PROCESSING
        jobs[job_id]["updated_at"] = datetime.now()

        logger.info(f"Processing text for job {job_id}: {request.title}")

        # Chunk text
        metadata = request.metadata or {}
        metadata["title"] = request.title
        metadata["document_type"] = DocumentType.TEXT
        metadata["job_id"] = job_id

        chunks = pdf_processor.chunk_text(request.text, metadata)

        # Store in vector database
        docs_added = vector_store.add_documents(chunks)

        # Update job
        jobs[job_id]["status"] = ProcessingStatus.COMPLETED
        jobs[job_id]["chunks_processed"] = len(chunks)
        jobs[job_id]["total_chunks"] = len(chunks)
        jobs[job_id]["updated_at"] = datetime.now()

        logger.info(f"Job {job_id} completed: {docs_added} documents added")

    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        jobs[job_id]["status"] = ProcessingStatus.FAILED
        jobs[job_id]["error_message"] = str(e)
        jobs[job_id]["updated_at"] = datetime.now()


@app.post("/process/text", response_model=ProcessingResponse, tags=["Processing"])
async def process_text(request: ProcessTextRequest, background_tasks: BackgroundTasks):
    """Process raw text"""
    # Create job
    job_id = f"text-{int(time.time())}"

    jobs[job_id] = {
        "job_id": job_id,
        "document_type": DocumentType.TEXT,
        "status": ProcessingStatus.PENDING,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "chunks_processed": 0,
        "total_chunks": 0,
        "error_message": None,
        "metadata": {
            "title": request.title,
        },
    }

    # Start background processing
    background_tasks.add_task(process_text_task, job_id, request)

    return ProcessingResponse(
        job_id=job_id,
        status=ProcessingStatus.PENDING,
        message="Text processing started",
        estimated_time_seconds=10,
    )


@app.get("/jobs/{job_id}", response_model=JobStatusResponse, tags=["Jobs"])
async def get_job_status(job_id: str):
    """Get status of a processing job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    # Calculate progress
    progress = 0.0
    if job["total_chunks"] > 0:
        progress = (job["chunks_processed"] / job["total_chunks"]) * 100
    elif job["status"] == ProcessingStatus.COMPLETED:
        progress = 100.0

    return JobStatusResponse(
        job_id=job["job_id"],
        status=job["status"],
        progress=progress,
        chunks_processed=job["chunks_processed"],
        total_chunks=job["total_chunks"],
        created_at=job["created_at"],
        updated_at=job["updated_at"],
        error_message=job.get("error_message"),
    )


@app.get("/jobs", tags=["Jobs"])
async def list_jobs(limit: int = 10, status: str = None):
    """List all processing jobs"""
    jobs_list = list(jobs.values())

    # Filter by status if provided
    if status:
        jobs_list = [j for j in jobs_list if j["status"] == status]

    # Sort by created_at descending
    jobs_list.sort(key=lambda x: x["created_at"], reverse=True)

    # Limit results
    jobs_list = jobs_list[:limit]

    return {"jobs": jobs_list, "total": len(jobs_list)}


@app.get("/query", tags=["Query"])
async def query_documents(q: str, k: int = 5):
    """Query vector store for relevant documents"""
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")

    try:
        results = vector_store.query(q, n_results=k)
        return {
            "query": q,
            "results": results,
            "count": len(results),
        }
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", tags=["General"])
async def get_stats():
    """Get service statistics"""
    return {
        "vector_store": {
            "total_documents": vector_store.count(),
        },
        "jobs": {
            "total": len(jobs),
            "pending": len([j for j in jobs.values() if j["status"] == ProcessingStatus.PENDING]),
            "processing": len([j for j in jobs.values() if j["status"] == ProcessingStatus.PROCESSING]),
            "completed": len([j for j in jobs.values() if j["status"] == ProcessingStatus.COMPLETED]),
            "failed": len([j for j in jobs.values() if j["status"] == ProcessingStatus.FAILED]),
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)
