from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TechStack, JourneyEntry, Project
from .serializers import TechStackSerializer, JourneyEntrySerializer, ProjectSerializer


class TechStackViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for tech stack items.
    """
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get tech stack grouped by category"""
        categories = {}
        for tech in self.queryset:
            category = tech.get_category_display()
            if category not in categories:
                categories[category] = []
            categories[category].append(TechStackSerializer(tech).data)
        return Response(categories)


class JourneyEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for journey entries.
    """
    queryset = JourneyEntry.objects.all().prefetch_related('tech_stack')
    serializer_class = JourneyEntrySerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for projects.
    """
    queryset = Project.objects.all().prefetch_related('tech_stack')
    serializer_class = ProjectSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured projects only"""
        featured = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)
