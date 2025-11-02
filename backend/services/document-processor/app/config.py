# Document Processor Service - Configuration
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Service Info
    service_name: str = "document-processor"
    service_version: str = "1.0.0"
    environment: str = "development"

    # Server
    port: int = 8003
    host: str = "0.0.0.0"

    # Django Backend
    django_api_url: str = "http://localhost:8000"

    # Google Cloud
    google_cloud_project: Optional[str] = None
    google_cloud_bucket: Optional[str] = None

    # ChromaDB
    chromadb_host: str = "localhost"
    chromadb_port: int = 8000
    chromadb_persist_directory: str = "./chromadb_data"

    # Processing
    max_file_size_mb: int = 50
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Vertex AI
    vertex_ai_location: str = "us-central1"
    vertex_ai_model: str = "textembedding-gecko@003"

    # CORS
    cors_origin: str = "*"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
