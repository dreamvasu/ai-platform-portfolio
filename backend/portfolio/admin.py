from django.contrib import admin
from .models import TechStack, JourneyEntry, Project, Paper, ScraperJob


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


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['title_short', 'source', 'category', 'published_date', 'relevance_score', 'is_featured', 'citation_count']
    list_filter = ['source', 'category', 'is_featured', 'published_date']
    search_fields = ['title', 'abstract', 'authors']
    ordering = ['-published_date', '-relevance_score']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'authors', 'abstract', 'published_date')
        }),
        ('Source', {
            'fields': ('source', 'source_id', 'url', 'pdf_url', 'github_url')
        }),
        ('Classification', {
            'fields': ('category', 'tags', 'relevance_score', 'citation_count')
        }),
        ('Display', {
            'fields': ('is_featured',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def title_short(self, obj):
        return obj.title[:80] + '...' if len(obj.title) > 80 else obj.title
    title_short.short_description = 'Title'


@admin.register(ScraperJob)
class ScraperJobAdmin(admin.ModelAdmin):
    list_display = ['source', 'start_time', 'status', 'papers_found', 'papers_added', 'papers_updated', 'duration_display']
    list_filter = ['source', 'status', 'start_time']
    search_fields = ['source', 'errors', 'log']
    ordering = ['-start_time']
    readonly_fields = ['start_time', 'duration']

    fieldsets = (
        ('Job Info', {
            'fields': ('source', 'status', 'start_time', 'end_time', 'duration')
        }),
        ('Statistics', {
            'fields': ('papers_found', 'papers_added', 'papers_updated')
        }),
        ('Logs', {
            'fields': ('errors', 'log'),
            'classes': ('collapse',)
        }),
    )

    def duration_display(self, obj):
        if obj.duration:
            mins = int(obj.duration // 60)
            secs = int(obj.duration % 60)
            return f"{mins}m {secs}s"
        return "-"
    duration_display.short_description = 'Duration'
