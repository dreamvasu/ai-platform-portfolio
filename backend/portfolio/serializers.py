from rest_framework import serializers
from .models import TechStack, JourneyEntry, Project


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
