from django.contrib import admin
from .models import TechStack, JourneyEntry, Project


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency_level', 'created_at']
    list_filter = ['category']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']


@admin.register(JourneyEntry)
class JourneyEntryAdmin(admin.ModelAdmin):
    list_display = ['hour', 'title', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['tech_stack']
    ordering = ['hour']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'github_url', 'live_url', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['tech_stack']
    ordering = ['-created_at']
