from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TechStackViewSet, JourneyEntryViewSet, ProjectViewSet,
    PaperViewSet, ScraperJobViewSet, populate_database
)
from .webhooks import (
    scraper_complete_webhook,
    document_processed_webhook,
    webhook_health
)

router = DefaultRouter()
router.register(r'tech-stack', TechStackViewSet, basename='techstack')
router.register(r'journey', JourneyEntryViewSet, basename='journey')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'papers', PaperViewSet, basename='paper')
router.register(r'scraper-jobs', ScraperJobViewSet, basename='scraperjob')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/populate/', populate_database, name='populate_database'),

    # Webhook endpoints for microservices
    path('webhooks/health/', webhook_health, name='webhook_health'),
    path('webhooks/scraper-complete/', scraper_complete_webhook, name='scraper_complete'),
    path('webhooks/document-processed/', document_processed_webhook, name='document_processed'),
]
