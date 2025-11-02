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


class Paper(models.Model):
    """ML/AI Research Papers"""
    CATEGORY_CHOICES = [
        ('llm', 'Large Language Models'),
        ('cv', 'Computer Vision'),
        ('rag', 'RAG & Embeddings'),
        ('mlops', 'MLOps & Platform'),
        ('training', 'Training & Optimization'),
        ('inference', 'Inference & Deployment'),
        ('nlp', 'Natural Language Processing'),
        ('multimodal', 'Multimodal AI'),
    ]

    SOURCE_CHOICES = [
        ('arxiv', 'arXiv'),
        ('huggingface', 'Hugging Face'),
        ('paperswithcode', 'Papers with Code'),
        ('scholar', 'Google Scholar'),
    ]

    title = models.CharField(max_length=500)
    abstract = models.TextField()
    authors = models.TextField(help_text="Comma-separated list of authors")
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    source_id = models.CharField(max_length=200, unique=True, help_text="Unique ID from source")
    url = models.URLField()
    pdf_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    published_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tags = models.JSONField(default=list, help_text='["transformers", "attention", ...]')
    citation_count = models.IntegerField(default=0)
    relevance_score = models.FloatField(default=0.0, help_text="0-1 score based on relevance")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-relevance_score']
        verbose_name_plural = "Papers"
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['category']),
            models.Index(fields=['source']),
        ]

    def __str__(self):
        return f"{self.title[:100]} ({self.get_source_display()})"


class ScraperJob(models.Model):
    """History of scraper job runs"""
    STATUS_CHOICES = [
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    source = models.CharField(max_length=50)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running')
    papers_found = models.IntegerField(default=0)
    papers_added = models.IntegerField(default=0)
    papers_updated = models.IntegerField(default=0)
    errors = models.TextField(blank=True)
    log = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_time']
        verbose_name_plural = "Scraper Jobs"

    def __str__(self):
        return f"{self.source} - {self.start_time} ({self.status})"

    @property
    def duration(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
