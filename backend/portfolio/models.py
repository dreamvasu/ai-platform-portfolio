from django.db import models
from django.utils import timezone


class TechStack(models.Model):
    """Technologies used in the portfolio"""
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('infrastructure', 'Infrastructure'),
        ('ai_ml', 'AI/ML'),
        ('database', 'Database'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    color = models.CharField(max_length=20, default='blue')  # Tailwind color
    proficiency_level = models.IntegerField(default=1)  # 1-5 scale
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['category', 'name']
        verbose_name_plural = "Tech Stack"

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class JourneyEntry(models.Model):
    """Hour-by-hour learning journey entries"""
    hour = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="What I learned")
    challenges = models.TextField(help_text="Challenges faced")
    outcomes = models.TextField(help_text="What I built")
    tech_stack = models.ManyToManyField(TechStack, related_name='journey_entries')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['hour']
        verbose_name_plural = "Journey Entries"

    def __str__(self):
        return f"Hour {self.hour}: {self.title}"


class Project(models.Model):
    """Projects/Deployments showcase"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.ManyToManyField(TechStack, related_name='projects')
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
