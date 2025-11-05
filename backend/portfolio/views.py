from rest_framework import viewsets, filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.management import call_command
from django.utils import timezone
from datetime import timedelta, datetime
from .models import TechStack, JourneyEntry, Project, Paper, ScraperJob
from .serializers import (
    TechStackSerializer, JourneyEntrySerializer, ProjectSerializer,
    PaperSerializer, PaperListSerializer, ScraperJobSerializer
)
import base64
import os
from google.cloud import vision
from vertexai.generative_models import GenerativeModel
import vertexai


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


@api_view(['POST'])
def populate_database(request):
    """Admin endpoint to populate database with production data"""
    try:
        call_command('populate_production_data')
        return Response({
            'status': 'success',
            'tech_stack': TechStack.objects.count(),
            'journey': JourneyEntry.objects.count(),
            'projects': Project.objects.count()
        })
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)


@api_view(['POST'])
def populate_blogs(request):
    """Admin endpoint to populate blog posts"""
    try:
        call_command('populate_blogs')
        return Response({
            'status': 'success',
            'message': 'Blog posts populated successfully',
            'total_papers': Paper.objects.count(),
            'featured_papers': Paper.objects.filter(is_featured=True).count()
        })
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)


@api_view(['POST'])
def upload_tech_sop(request):
    """
    Upload an image containing Tech SOP, extract text with OCR,
    generate blog post with AI, and save to database
    """
    try:
        # Check if image was uploaded
        if 'image' not in request.FILES:
            return Response({
                'status': 'error',
                'message': 'No image file provided'
            }, status=400)

        image_file = request.FILES['image']

        # Read image content
        image_content = image_file.read()

        # Step 1: Extract text from image using Google Cloud Vision
        print("🔍 Extracting text from image...")
        vision_client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_content)
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations

        if not texts:
            return Response({
                'status': 'error',
                'message': 'No text found in image'
            }, status=400)

        extracted_text = texts[0].description
        print(f"✓ Extracted {len(extracted_text)} characters")

        # Step 2: Generate blog post using Vertex AI Gemini
        print("🤖 Generating blog post from extracted text...")
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        vertexai.init(project=project_id, location="us-central1")

        model = GenerativeModel("gemini-pro")

        prompt = f"""You are a technical writer. Based on the following extracted text from a Tech SOP (Standard Operating Procedure) image, create a comprehensive technical blog post.

The extracted text is:
---
{extracted_text}
---

Please create a blog post with the following format:

1. **Title**: A clear, concise title (50-80 characters)
2. **Content**: A well-structured blog post (1500-2500 words) that includes:
   - **Introduction**: Explain what this SOP covers
   - **Key Steps**: Break down the procedure into clear sections
   - **Code Examples**: If applicable, include any commands or code snippets
   - **Best Practices**: Highlight important tips and recommendations
   - **Common Pitfalls**: What to avoid
   - **Conclusion**: Summary of key takeaways

Use markdown formatting with headers, bullet points, code blocks, and emphasis where appropriate.
Write in first-person ("I implemented this...") as if sharing personal experience.

Return ONLY a JSON object with this structure:
{{
  "title": "Your title here",
  "content": "Your full blog post content in markdown format here",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}}

Do not include any explanation outside the JSON."""

        generation_response = model.generate_content(prompt)
        blog_content = generation_response.text

        # Parse JSON response
        import json
        # Clean the response (remove markdown code blocks if present)
        blog_content = blog_content.strip()
        if blog_content.startswith('```json'):
            blog_content = blog_content[7:]
        if blog_content.startswith('```'):
            blog_content = blog_content[3:]
        if blog_content.endswith('```'):
            blog_content = blog_content[:-3]
        blog_content = blog_content.strip()

        blog_data = json.loads(blog_content)

        # Step 3: Save image to Cloud Storage (optional - for now we'll skip and use base64)
        # In production, you'd save to Cloud Storage and get a public URL
        # For now, we'll just note the image was processed

        # Step 4: Create blog post in database
        print("💾 Saving blog post to database...")

        # Generate slug from title
        slug = blog_data['title'].lower().replace(' ', '-').replace(':', '').replace('&', 'and')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')[:100]

        # Create blog post
        blog_post = Paper.objects.create(
            title=blog_data['title'],
            abstract=blog_data['content'],
            authors='Vasu Kapoor',
            source='blog',
            source_id=f"tech-sop-{slug}",
            url=None,
            published_date=datetime.now().date(),
            category='mlops',
            tags=blog_data.get('tags', []),
            citation_count=0,
            relevance_score=0.90,
            is_featured=False
        )

        print(f"✅ Blog post created: {blog_post.title}")

        return Response({
            'status': 'success',
            'message': 'Tech SOP processed and blog post created successfully',
            'blog_post': {
                'id': blog_post.id,
                'title': blog_post.title,
                'slug': blog_post.source_id,
                'url': f'/blog/{blog_post.id}',
                'extracted_text_length': len(extracted_text),
                'blog_content_length': len(blog_data['content']),
                'tags': blog_data.get('tags', [])
            }
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


class PaperPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PaperViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for ML/AI research papers.

    Supports filtering by:
    - category: llm, cv, rag, mlops, training, inference, nlp, multimodal
    - source: arxiv, huggingface, paperswithcode, scholar
    - featured: true/false
    - search: search in title and abstract
    """
    queryset = Paper.objects.all()
    pagination_class = PaperPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'abstract', 'authors', 'tags']
    ordering_fields = ['published_date', 'relevance_score', 'citation_count', 'created_at']
    ordering = ['-published_date', '-relevance_score']

    def get_serializer_class(self):
        if self.action == 'list':
            return PaperListSerializer
        return PaperSerializer

    def get_queryset(self):
        queryset = Paper.objects.all()

        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        # Filter by source
        source = self.request.query_params.get('source', None)
        if source:
            queryset = queryset.filter(source=source)

        # Filter by featured
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)

        # Filter by days (papers from last N days)
        days = self.request.query_params.get('days', None)
        if days:
            try:
                days_int = int(days)
                cutoff_date = timezone.now().date() - timedelta(days=days_int)
                queryset = queryset.filter(published_date__gte=cutoff_date)
            except ValueError:
                pass

        return queryset

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get papers from last 30 days"""
        cutoff_date = timezone.now().date() - timedelta(days=30)
        papers = self.queryset.filter(published_date__gte=cutoff_date)
        serializer = PaperListSerializer(papers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending papers (high relevance + recent)"""
        cutoff_date = timezone.now().date() - timedelta(days=60)
        papers = self.queryset.filter(
            published_date__gte=cutoff_date,
            relevance_score__gte=0.7
        ).order_by('-citation_count', '-relevance_score', '-published_date')[:20]
        serializer = PaperListSerializer(papers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get papers grouped by category"""
        categories = {}
        for choice in Paper.CATEGORY_CHOICES:
            category_key = choice[0]
            category_name = choice[1]
            papers = self.queryset.filter(category=category_key)[:10]
            categories[category_key] = {
                'name': category_name,
                'papers': PaperListSerializer(papers, many=True).data
            }
        return Response(categories)

    @action(detail=False, methods=['post'])
    def scrape(self, request):
        """Trigger manual scraping (admin only)"""
        try:
            source = request.data.get('source', 'arxiv')
            days = request.data.get('days', 7)

            # Run scraper command
            call_command('scrape_papers', source=source, days=days)

            return Response({
                'status': 'success',
                'message': f'Scraping {source} for papers from last {days} days',
                'papers': Paper.objects.count()
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=500)


class ScraperJobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for scraper job history.
    """
    queryset = ScraperJob.objects.all()
    serializer_class = ScraperJobSerializer
    ordering = ['-start_time']

    def get_queryset(self):
        queryset = ScraperJob.objects.all()

        # Filter by source
        source = self.request.query_params.get('source', None)
        if source:
            queryset = queryset.filter(source=source)

        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest job for each source"""
        latest_jobs = {}
        for source in ['arxiv', 'huggingface', 'paperswithcode']:
            job = self.queryset.filter(source=source).first()
            if job:
                latest_jobs[source] = ScraperJobSerializer(job).data
        return Response(latest_jobs)
