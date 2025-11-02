import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portfolio.models import Project

Project.objects.create(
    name="Calibra - Enterprise Calibration Platform",
    slug="calibra",
    description="Multi-tenant SaaS platform for scientific instrument calibration management. Deployed on Azure with 99.9% uptime, processing 10K+ calibration requests annually.",
    long_description="""
Enterprise-grade calibration management platform serving 20+ clients with complete data isolation using django-tenants.

Key Features:
- Multi-tenant architecture with PostgreSQL schema isolation
- Event-sourced state management for full audit trails
- Async PDF generation handling 500+ certificates daily
- Complex scientific calculations and regulatory compliance
- Azure deployment with auto-scaling and high availability

Technical Stack: Django, PostgreSQL, Redis, Celery, Azure App Service, Terraform, Docker
""",
    tech_stack="Django, Django REST Framework, PostgreSQL, Redis, Celery, Azure App Service, Azure Blob Storage, Terraform, Docker, GitLab CI/CD",
    github_url="https://github.com/dreamvasu/calibra-platform",
    live_url="https://calibra.azure.com",
    case_study_url="/case-studies/calibra",
    featured=True,
    category="Production Systems",
    display_order=1
)

print("✅ Calibra project added!")
