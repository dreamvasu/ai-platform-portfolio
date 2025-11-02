import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portfolio.models import Project, TechStack

# Get tech stack items
tech_items = TechStack.objects.filter(name__in=[
    'Django', 'Django REST Framework', 'PostgreSQL', 'Terraform', 'Docker'
])

project = Project.objects.create(
    title="Calibra - Enterprise Calibration Platform",
    description="Multi-tenant SaaS platform for scientific instrument calibration management. Deployed on Azure with 99.9% uptime, processing 10K+ calibration requests annually. Enterprise-grade platform serving 20+ clients with complete data isolation using django-tenants. Multi-tenant architecture with PostgreSQL schema isolation, event-sourced state management for full audit trails, async PDF generation handling 500+ certificates daily. Complex scientific calculations and regulatory compliance.",
    github_url="https://github.com/dreamvasu/calibra-platform",
    live_url="https://calibra.azure.com",
    is_featured=True
)
project.tech_stack.set(tech_items)

print("✅ Calibra project added!")
