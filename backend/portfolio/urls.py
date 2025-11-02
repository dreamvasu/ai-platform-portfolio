from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TechStackViewSet, JourneyEntryViewSet, ProjectViewSet,
    PaperViewSet, ScraperJobViewSet, populate_database
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
]
