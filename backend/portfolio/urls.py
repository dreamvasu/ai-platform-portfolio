from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TechStackViewSet, JourneyEntryViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'tech-stack', TechStackViewSet, basename='techstack')
router.register(r'journey', JourneyEntryViewSet, basename='journey')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]
