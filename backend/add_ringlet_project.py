import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portfolio.models import Project

Project.objects.create(
    name="Ringlet - Educational Platform on Kubernetes",
    slug="ringlet",
    description="Django-based educational platform containerized and deployed on Kubernetes with full autoscaling, monitoring, and production-ready infrastructure using Helm charts.",
    long_description="""
Comprehensive Kubernetes deployment architecture for Ringlet, a Django-based online learning management system.

Key Features:
- Multi-stage Docker optimization reducing image size by 60%
- Kubernetes orchestration with PostgreSQL, Redis, and Celery workers
- Horizontal Pod Autoscaler (HPA) for automatic scaling (3-10 pods)
- Helm charts for parameterized multi-environment deployments
- Production-ready with health checks, resource limits, and zero-downtime updates
- Complete Infrastructure as Code using Kustomize and Helm

Technical Stack: Django, PostgreSQL, Redis, Celery, Kubernetes, Docker, Helm, GKE, Gunicorn
""",
    tech_stack="Django 4.x, PostgreSQL 15, Redis 7, Celery, Kubernetes, Docker, Helm 3, Kustomize, GKE, Gunicorn, Python 3.11",
    github_url="https://github.com/dreamvasu/ringlet",
    live_url="https://ringlet.example.com",
    case_study_url="/case-studies/ringlet",
    featured=True,
    category="Platform Engineering",
    display_order=2
)

print("✅ Ringlet project added!")
