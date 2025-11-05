"""
Webhook endpoints for microservices integration.

These endpoints receive data from our microservices:
- Paper Scraper: POST scraped papers
- Document Processor: POST processed documents
- Analytics: POST events (optional)
"""

import os
import logging
from functools import wraps
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Paper, ScraperJob
from .serializers import PaperSerializer

logger = logging.getLogger(__name__)

# Webhook authentication using shared secret
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', 'dev-secret-change-in-production')


def verify_webhook_signature(view_func):
    """
    Decorator to verify webhook requests using shared secret.

    In production, this should be replaced with:
    - Cloud Run IAM authentication
    - JWT tokens
    - HMAC signatures
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Get the authorization header
        auth_header = request.headers.get('Authorization', '')

        # Check if it's a Bearer token
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
        else:
            token = request.headers.get('X-Webhook-Secret', '')

        # Verify the token matches our secret
        if token != WEBHOOK_SECRET:
            logger.warning(f"Invalid webhook signature from {request.META.get('REMOTE_ADDR')}")
            return Response(
                {'error': 'Invalid webhook signature'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return view_func(request, *args, **kwargs)

    return wrapped_view


@api_view(['POST'])
@permission_classes([AllowAny])
@verify_webhook_signature
def scraper_complete_webhook(request):
    """
    Webhook endpoint for Paper Scraper service.

    Expected payload:
    {
        "job_id": "arxiv-1699000000",
        "source": "arxiv",
        "papers": [
            {
                "title": "Paper Title",
                "abstract": "Abstract...",
                "authors": ["Author 1", "Author 2"],
                "url": "https://arxiv.org/abs/...",
                "pdf_url": "https://arxiv.org/pdf/...",
                "published_date": "2025-11-03",
                "category": "llm",
                "relevance_score": 0.85,
                "tags": ["tag1", "tag2"]
            }
        ],
        "total_papers": 10,
        "timestamp": "2025-11-03T12:00:00Z"
    }
    """
    try:
        data = request.data
        job_id = data.get('job_id')
        source = data.get('source', 'arxiv')
        papers_data = data.get('papers', [])

        logger.info(f"Received webhook from scraper: job_id={job_id}, papers={len(papers_data)}")

        # Create scraper job record
        scraper_job = ScraperJob.objects.create(
            source=source,
            status='completed',
            papers_found=len(papers_data),
            end_time=timezone.now(),
            log=f"Webhook received from scraper. Job ID: {job_id}"
        )

        # Store each paper in the database
        papers_created = 0
        papers_updated = 0

        for paper_data in papers_data:
            # Check if paper already exists (by URL)
            paper_url = paper_data.get('url', '')

            if paper_url:
                # Use source_id from scraper if provided, otherwise extract from URL
                source_id = paper_data.get('source_id')
                if not source_id:
                    source_id = paper_url.split('/')[-1] if '/' in paper_url else paper_url

                # Convert authors list to comma-separated string
                authors = paper_data.get('authors', [])
                if isinstance(authors, list):
                    authors_str = ', '.join(authors)
                else:
                    authors_str = authors

                paper, created = Paper.objects.update_or_create(
                    url=paper_url,
                    defaults={
                        'title': paper_data.get('title', ''),
                        'abstract': paper_data.get('abstract', ''),
                        'authors': authors_str,
                        'source_id': source_id,
                        'pdf_url': paper_data.get('pdf_url', ''),
                        'published_date': paper_data.get('published_date'),
                        'source': source,
                        'category': paper_data.get('category', 'mlops'),
                        'relevance_score': paper_data.get('relevance_score', 0.5),
                        'tags': paper_data.get('tags', []),
                        'citation_count': paper_data.get('citation_count', 0),
                    }
                )

                if created:
                    papers_created += 1
                    scraper_job.papers_added += 1
                else:
                    papers_updated += 1
                    scraper_job.papers_updated += 1

        scraper_job.save()

        logger.info(f"Processed {papers_created} new papers, updated {papers_updated} existing papers")

        return Response({
            'status': 'success',
            'job_id': job_id,
            'papers_created': papers_created,
            'papers_updated': papers_updated,
            'total_papers': len(papers_data)
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error processing scraper webhook: {str(e)}")
        return Response(
            {'error': 'Failed to process webhook', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@verify_webhook_signature
def document_processed_webhook(request):
    """
    Webhook endpoint for Document Processor service.

    Expected payload:
    {
        "job_id": "pdf-1699000000",
        "document_type": "pdf",
        "title": "Document Title",
        "url": "https://example.com/doc.pdf",
        "chunks_processed": 15,
        "status": "completed",
        "metadata": {
            "author": "John Doe",
            "category": "research"
        },
        "timestamp": "2025-11-03T12:00:00Z"
    }
    """
    try:
        data = request.data
        job_id = data.get('job_id')
        document_type = data.get('document_type', 'unknown')
        title = data.get('title', 'Untitled')
        chunks = data.get('chunks_processed', 0)

        logger.info(f"Received webhook from document processor: job_id={job_id}, title={title}, chunks={chunks}")

        # For now, just log the webhook data
        # In the future, we can:
        # 1. Create a Document model to track processed documents
        # 2. Store document metadata
        # 3. Link documents to projects or papers
        # 4. Track which documents are in the RAG system

        return Response({
            'status': 'success',
            'job_id': job_id,
            'message': f'Document "{title}" processed successfully with {chunks} chunks'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error processing document webhook: {str(e)}")
        return Response(
            {'error': 'Failed to process webhook', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def webhook_health(request):
    """Health check endpoint for webhooks"""
    return Response({
        'status': 'healthy',
        'service': 'django-webhooks',
        'timestamp': timezone.now().isoformat(),
        'endpoints': {
            'scraper_complete': '/api/webhooks/scraper-complete/',
            'document_processed': '/api/webhooks/document-processed/',
            'fix_blog_slugs': '/api/webhooks/fix-blog-slugs/'
        }
    })


@api_view(['POST'])
@permission_classes([AllowAny])
@verify_webhook_signature
def fix_blog_slugs_webhook(request):
    """
    Webhook endpoint to fix blog post slugs.

    Expected payload:
    {
        "dry_run": false
    }
    """
    try:
        from django.utils.text import slugify

        dry_run = request.data.get('dry_run', False)

        logger.info(f"Starting blog slug fix (dry_run={dry_run})")

        # Find blog posts without source_id
        from django.db.models import Q
        blogs_without_slug = Paper.objects.filter(
            Q(source='blog') | Q(source='blogs')
        ).filter(
            Q(source_id__isnull=True) | Q(source_id='')
        )

        total = blogs_without_slug.count()
        logger.info(f"Found {total} blog posts without slugs")

        if total == 0:
            return Response({
                'status': 'success',
                'message': 'All blog posts already have slugs',
                'total': 0,
                'updated': 0
            })

        updated = 0
        results = []

        for blog in blogs_without_slug:
            # Generate slug from URL or title
            if blog.url:
                parts = blog.url.rstrip('/').split('/')
                if len(parts) > 1 and parts[-1]:
                    slug = slugify(parts[-1])
                else:
                    slug = slugify(blog.title[:80])
            else:
                slug = slugify(blog.title[:80])

            # Ensure uniqueness
            base_slug = slug
            counter = 1
            while Paper.objects.filter(source_id=slug).exclude(id=blog.id).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            if not dry_run:
                blog.source_id = slug
                blog.save()
                updated += 1

            results.append({
                'id': blog.id,
                'title': blog.title[:50],
                'slug': slug
            })

        logger.info(f"Blog slug fix completed: {updated} updated (dry_run={dry_run})")

        return Response({
            'status': 'success',
            'dry_run': dry_run,
            'total': total,
            'updated': updated,
            'results': results[:10]  # Limit to first 10 for response size
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error fixing blog slugs: {str(e)}")
        return Response(
            {'error': 'Failed to fix blog slugs', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
