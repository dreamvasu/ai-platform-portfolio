"""
Configuration management for Paper Scraper Service
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Service
    service_name: str = "paper-scraper"
    service_version: str = "1.0.0"
    environment: str = "development"
    port: int = 8001

    # Django Backend
    django_api_url: str = "http://localhost:8000"
    django_api_key: Optional[str] = None
    webhook_secret: str = "dev-secret-change-in-production"  # Must match Django WEBHOOK_SECRET

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Scraping
    max_results_per_source: int = 100
    request_timeout: int = 30
    rate_limit_delay: float = 1.0

    # arXiv
    arxiv_base_url: str = "http://export.arxiv.org/api/query"

    # Health Check
    health_check_enabled: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
