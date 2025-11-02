from rest_framework import serializers
from .models import TechStack, JourneyEntry, Project, Paper, ScraperJob


class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ['id', 'name', 'category', 'description', 'color', 'proficiency_level', 'created_at']


class JourneyEntrySerializer(serializers.ModelSerializer):
    tech_stack = TechStackSerializer(many=True, read_only=True)

    class Meta:
        model = JourneyEntry
        fields = ['id', 'hour', 'title', 'description', 'challenges', 'outcomes', 'tech_stack', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    tech_stack = TechStackSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'tech_stack', 'github_url', 'live_url', 'image_url', 'is_featured', 'created_at', 'updated_at']


class PaperSerializer(serializers.ModelSerializer):
    source_display = serializers.CharField(source='get_source_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    authors_list = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        fields = [
            'id', 'title', 'abstract', 'authors', 'authors_list',
            'source', 'source_display', 'source_id', 'url', 'pdf_url', 'github_url',
            'published_date', 'category', 'category_display', 'tags',
            'citation_count', 'relevance_score', 'is_featured',
            'created_at', 'updated_at'
        ]

    def get_authors_list(self, obj):
        """Convert comma-separated authors to list"""
        return [author.strip() for author in obj.authors.split(',') if author.strip()]


class PaperListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    source_display = serializers.CharField(source='get_source_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Paper
        fields = [
            'id', 'title', 'authors', 'source', 'source_display',
            'url', 'pdf_url', 'published_date', 'category', 'category_display',
            'citation_count', 'relevance_score', 'is_featured', 'tags'
        ]


class ScraperJobSerializer(serializers.ModelSerializer):
    duration = serializers.ReadOnlyField()

    class Meta:
        model = ScraperJob
        fields = [
            'id', 'source', 'start_time', 'end_time', 'status',
            'papers_found', 'papers_added', 'papers_updated',
            'errors', 'log', 'duration'
        ]
