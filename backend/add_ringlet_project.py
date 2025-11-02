import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portfolio.models import Project, TechStack

# Get tech stack items
tech_items = TechStack.objects.filter(name__in=[
    'Django', 'Kubernetes', 'Docker', 'PostgreSQL'
])

project = Project.objects.create(
    title="Ringlet - Educational Platform on Kubernetes",
    description="Django-based educational platform containerized and deployed on Kubernetes with full autoscaling, monitoring, and production-ready infrastructure using Helm charts. Comprehensive K8s deployment with PostgreSQL, Redis, Celery workers, HPA (3-10 pods), Helm charts for multi-environment deployments. Multi-stage Docker optimization reducing image size by 60%. Production-ready with health checks, resource limits, and zero-downtime updates.",
    github_url="https://github.com/dreamvasu/ringlet",
    live_url="https://ringlet.example.com",
    is_featured=True
)
project.tech_stack.set(tech_items)

print("✅ Ringlet project added!")
