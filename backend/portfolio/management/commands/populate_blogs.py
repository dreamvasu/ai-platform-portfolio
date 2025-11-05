"""
Management command to populate the database with technical blog posts
Based on portfolio documentation and case studies
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from portfolio.models import Paper


class Command(BaseCommand):
    help = 'Populate database with technical blog posts from portfolio content'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Populating blog posts...'))

        # Clear existing papers first (optional)
        Paper.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing blog posts'))

        blog_posts = [
            {
                'title': 'Production Kubernetes Deployment: A Complete Guide to Azure AKS',
                'abstract': '''A comprehensive walkthrough of deploying a Django-based Learning Management System to Azure Kubernetes Service (AKS). This guide covers everything from infrastructure provisioning with Terraform to implementing autoscaling, health checks, and zero-downtime deployments. Learn how to configure StatefulSets for databases, implement Horizontal Pod Autoscaling (HPA), and design a production-grade multi-component architecture with Django, Celery workers, PostgreSQL, and Redis. Includes complete Terraform modules, Kubernetes manifests, and troubleshooting guides. Perfect for platform engineers looking to master AKS deployments.''',
                'authors': 'Vasu Kapoor',
                'source': 'huggingface',
                'source_id': 'vasu-k8s-aks-deployment-guide',
                'url': 'https://vasukapoor.com/blog/kubernetes-aks-deployment',
                'published_date': (datetime.now() - timedelta(days=2)).date(),
                'category': 'mlops',
                'tags': ['Kubernetes', 'Azure AKS', 'Terraform', 'Docker', 'DevOps', 'Platform Engineering'],
                'citation_count': 45,
                'relevance_score': 0.95,
                'is_featured': True
            },
            {
                'title': 'Building Production RAG Systems: From Theory to Deployment',
                'abstract': '''A hands-on guide to building production-grade Retrieval-Augmented Generation (RAG) systems using Google Vertex AI, ChromaDB, and Django REST Framework. Learn how to implement document ingestion pipelines, generate embeddings with Vertex AI textembedding-gecko, design efficient vector stores, and create intelligent query systems. Covers real-world optimizations including caching strategies, chunk sizing, semantic search, and deployment to Google Cloud Run. Includes complete code examples, API design patterns, and performance benchmarks. This guide demonstrates how to build an AI chatbot that answers questions about technical documentation with 85%+ accuracy.''',
                'authors': 'Vasu Kapoor',
                'source': 'huggingface',
                'source_id': 'vasu-rag-production-guide',
                'url': 'https://vasukapoor.com/blog/rag-production-systems',
                'published_date': (datetime.now() - timedelta(days=5)).date(),
                'category': 'rag',
                'tags': ['RAG', 'LLM', 'Vertex AI', 'Embeddings', 'ChromaDB', 'Django', 'GCP'],
                'citation_count': 78,
                'relevance_score': 0.98,
                'is_featured': True
            },
            {
                'title': 'Multi-Tenant SaaS Architecture: Schema Isolation at Scale',
                'abstract': '''Deep dive into building a multi-tenant SaaS platform using PostgreSQL schema-based isolation. Learn how to design tenant-aware Django applications with django-tenants, implement zero data leakage architectures, and handle cross-tenant migrations safely. This guide covers production challenges including tenant routing via subdomains, automated provisioning, backup strategies, and performance optimization for 20+ tenants processing 500K+ API requests daily. Includes real-world code examples from Calibra, a production calibration management platform deployed on Azure App Service. Essential reading for platform engineers building B2B SaaS applications.''',
                'authors': 'Vasu Kapoor',
                'source': 'arxiv',
                'source_id': 'vasu-multitenant-saas-2024',
                'url': 'https://vasukapoor.com/blog/multi-tenant-saas-architecture',
                'published_date': (datetime.now() - timedelta(days=8)).date(),
                'category': 'mlops',
                'tags': ['Multi-tenancy', 'SaaS', 'PostgreSQL', 'Django', 'Azure', 'Architecture'],
                'citation_count': 62,
                'relevance_score': 0.92,
                'is_featured': True
            },
            {
                'title': 'Infrastructure as Code with Terraform: Modular Architecture for Multi-Cloud',
                'abstract': '''Master Infrastructure as Code (IaC) with Terraform by building reusable modules for Azure and GCP deployments. This guide walks through creating production-grade Terraform modules for networking (VNets, subnets, NSGs), Kubernetes clusters (AKS, GKE), container registries (ACR, GCR), and storage solutions. Learn best practices for module composition, state management with remote backends, environment isolation (dev/staging/prod), and handling resource dependencies. Includes complete working examples deploying a Django application to Azure AKS with autoscaling, monitoring, and security configurations. Written for platform engineers managing cloud infrastructure at scale.''',
                'authors': 'Vasu Kapoor',
                'source': 'paperswithcode',
                'source_id': 'vasu-terraform-iac-guide-2024',
                'url': 'https://vasukapoor.com/blog/terraform-iac-multi-cloud',
                'published_date': (datetime.now() - timedelta(days=10)).date(),
                'category': 'mlops',
                'tags': ['Terraform', 'IaC', 'Azure', 'GCP', 'DevOps', 'Cloud Infrastructure'],
                'citation_count': 54,
                'relevance_score': 0.90,
                'is_featured': False
            },
            {
                'title': 'Horizontal Pod Autoscaling in Kubernetes: Configuration and Best Practices',
                'abstract': '''A practical guide to implementing Horizontal Pod Autoscaling (HPA) in production Kubernetes environments. Learn how to configure HPA based on CPU and memory metrics, design scale-up and scale-down behaviors to prevent flapping, and set appropriate stabilization windows. This guide includes real-world examples from a Django application scaling from 3 to 10 pods, handling 5x peak load (5000 concurrent users), and maintaining sub-500ms response times. Covers metrics-server setup, resource requests/limits, custom metrics with Prometheus, and troubleshooting common HPA issues. Essential for platform engineers optimizing Kubernetes workloads for cost and performance.''',
                'authors': 'Vasu Kapoor',
                'source': 'huggingface',
                'source_id': 'vasu-k8s-hpa-best-practices',
                'url': 'https://vasukapoor.com/blog/kubernetes-hpa-autoscaling',
                'published_date': (datetime.now() - timedelta(days=12)).date(),
                'category': 'mlops',
                'tags': ['Kubernetes', 'Autoscaling', 'HPA', 'Performance', 'Cloud Native'],
                'citation_count': 41,
                'relevance_score': 0.88,
                'is_featured': False
            },
            {
                'title': 'High Availability & Disaster Recovery for Cloud-Native Applications',
                'abstract': '''Comprehensive guide to designing HA/DR strategies for cloud-native applications. Learn how to implement multi-region architectures with global load balancers, configure database replication with read replicas, design automated failover procedures, and create disaster recovery runbooks. Covers SLA definitions (99.9% availability), RTO/RPO targets (15min/5min), monitoring with Cloud Operations, and cost optimization strategies. Includes production examples using Google Cloud Run, Cloud SQL, and Cloud Load Balancing. This guide demonstrates how to achieve enterprise-grade reliability ($106/month infrastructure) with automated health checks, backup strategies, and incident response procedures.''',
                'authors': 'Vasu Kapoor',
                'source': 'arxiv',
                'source_id': 'vasu-ha-dr-cloud-native-2024',
                'url': 'https://vasukapoor.com/blog/ha-dr-cloud-native',
                'published_date': (datetime.now() - timedelta(days=3)).date(),
                'category': 'mlops',
                'tags': ['HA/DR', 'Reliability', 'SRE', 'Cloud', 'GCP', 'Architecture'],
                'citation_count': 33,
                'relevance_score': 0.87,
                'is_featured': False
            },
            {
                'title': 'Docker Multi-Stage Builds: Optimizing Container Images for Production',
                'abstract': '''Learn how to optimize Docker images using multi-stage builds, reducing image size by 60% while improving security and build times. This guide covers separating build-time and runtime dependencies, implementing non-root users, layer caching strategies, and .dockerignore best practices. Real-world example shows reducing a Django application image from 1.2GB to 480MB, cutting deployment time by 40% and saving on registry storage costs. Includes complete Dockerfile examples for Python applications with dependency management, health checks, and production-ready configurations. Essential reading for platform engineers optimizing containerized workloads.''',
                'authors': 'Vasu Kapoor',
                'source': 'huggingface',
                'source_id': 'vasu-docker-multistage-optimization',
                'url': 'https://vasukapoor.com/blog/docker-multi-stage-builds',
                'published_date': (datetime.now() - timedelta(days=15)).date(),
                'category': 'mlops',
                'tags': ['Docker', 'Containers', 'Optimization', 'DevOps', 'Security'],
                'citation_count': 56,
                'relevance_score': 0.85,
                'is_featured': False
            },
            {
                'title': 'Async Task Processing with Celery: Scaling Background Jobs in Production',
                'abstract': '''Master asynchronous task processing with Celery for production Django applications. Learn how to design worker pools, implement task priority queues, configure Celery Beat for scheduled tasks, and handle failures with retry logic. This guide covers real-world PDF generation (142 PDFs/minute throughput), email campaigns, and data processing pipelines. Includes architecture patterns for singleton schedulers, worker autoscaling (2-6 pods), monitoring with Flower, and Redis as broker. Production examples show reducing API response times from 30s to <100ms by moving heavy computations to background workers. Complete with deployment configurations for Kubernetes and Azure App Service.''',
                'authors': 'Vasu Kapoor',
                'source': 'paperswithcode',
                'source_id': 'vasu-celery-async-processing-2024',
                'url': 'https://vasukapoor.com/blog/celery-async-task-processing',
                'published_date': (datetime.now() - timedelta(days=18)).date(),
                'category': 'mlops',
                'tags': ['Celery', 'Django', 'Async', 'Background Jobs', 'Redis', 'Scalability'],
                'citation_count': 47,
                'relevance_score': 0.84,
                'is_featured': False
            },
            {
                'title': 'Database Query Optimization: From 8 Seconds to 200ms',
                'abstract': '''A practical case study in database performance optimization for Django applications. Learn how to identify and fix N+1 query problems using select_related and prefetch_related, design efficient database indexes, implement query result caching with Redis, and use django-debug-toolbar for profiling. Real-world example shows optimizing a multi-tenant SaaS dashboard from 8.5s to 420ms (95% improvement), reducing database CPU from 85% to 35%, and supporting 1000+ concurrent users. Includes PostgreSQL-specific optimizations, connection pooling with PgBouncer, and monitoring strategies. Essential for backend engineers building data-intensive applications.''',
                'authors': 'Vasu Kapoor',
                'source': 'arxiv',
                'source_id': 'vasu-db-query-optimization-2024',
                'url': 'https://vasukapoor.com/blog/database-query-optimization',
                'published_date': (datetime.now() - timedelta(days=20)).date(),
                'category': 'mlops',
                'tags': ['Database', 'PostgreSQL', 'Performance', 'Django', 'Optimization'],
                'citation_count': 68,
                'relevance_score': 0.91,
                'is_featured': False
            },
            {
                'title': 'LLM Integration Patterns: Building AI-Powered Applications with GPT-4',
                'abstract': '''Comprehensive guide to integrating Large Language Models (LLMs) into production applications using Azure OpenAI Service. Learn prompt engineering techniques for structured output, implementing retry logic with exponential backoff, cost optimization through caching, and error handling strategies. Real-world example from Stiklaro educational platform shows generating interactive learning content (lessons, activities, assessments) from PDFs using GPT-4 with temperature tuning (0.7) for balanced creativity and accuracy. Covers API authentication, rate limiting, streaming responses, and migrating from OpenAI to Azure for enterprise compliance (GDPR, COPPA). Includes complete code examples and production deployment patterns.''',
                'authors': 'Vasu Kapoor',
                'source': 'huggingface',
                'source_id': 'vasu-llm-integration-gpt4-2024',
                'url': 'https://vasukapoor.com/blog/llm-integration-gpt4',
                'published_date': (datetime.now() - timedelta(days=7)).date(),
                'category': 'llm',
                'tags': ['GPT-4', 'LLM', 'Azure OpenAI', 'AI Integration', 'Prompt Engineering'],
                'citation_count': 89,
                'relevance_score': 0.96,
                'is_featured': True
            },
            {
                'title': 'Azure Document Intelligence: Extracting Structured Data from PDFs',
                'abstract': '''Learn how to extract structured content from PDFs using Azure Document Intelligence (formerly Form Recognizer). This guide covers the prebuilt-layout model for document structure analysis, extracting text with bounding boxes, table detection and cell-level extraction, and processing multi-page documents. Real-world example shows building an educational content pipeline that converts textbook PDFs into interactive learning modules, achieving 95%+ accuracy in layout understanding compared to 70-80% with basic OCR. Includes Python integration with DocumentIntelligenceClient, handling async operations with pollers, cost optimization strategies ($0.01 per page), and comparison with PyPDF2/pdfplumber alternatives.''',
                'authors': 'Vasu Kapoor',
                'source': 'paperswithcode',
                'source_id': 'vasu-azure-document-intelligence-2024',
                'url': 'https://vasukapoor.com/blog/azure-document-intelligence',
                'published_date': (datetime.now() - timedelta(days=25)).date(),
                'category': 'cv',
                'tags': ['Azure', 'Document Intelligence', 'OCR', 'Computer Vision', 'PDF Processing'],
                'citation_count': 38,
                'relevance_score': 0.83,
                'is_featured': False
            },
            {
                'title': 'Neural Text-to-Speech: Creating Character Voices for Interactive Applications',
                'abstract': '''A practical guide to implementing Azure Neural Text-to-Speech (TTS) for creating natural-sounding character voices in educational and interactive applications. Learn SSML (Speech Synthesis Markup Language) for prosody control, voice selection strategies for different characters (grandmother, child, narrator), and audio generation pipelines. Real-world example from children\'s learning platform shows configuring speech rate (0.9x for comprehension), pitch variation for character distinction, and natural pauses in dialogue. Covers batch audio generation, WAV format optimization, Azure Blob Storage integration for media assets, and cost management ($16 per 1M characters). Includes Python code with Azure Speech SDK and production deployment patterns.''',
                'authors': 'Vasu Kapoor',
                'source': 'huggingface',
                'source_id': 'vasu-neural-tts-azure-2024',
                'url': 'https://vasukapoor.com/blog/neural-tts-azure',
                'published_date': (datetime.now() - timedelta(days=22)).date(),
                'category': 'nlp',
                'tags': ['TTS', 'Speech Synthesis', 'Azure', 'Audio', 'Neural Networks'],
                'citation_count': 29,
                'relevance_score': 0.79,
                'is_featured': False
            },
            {
                'title': 'Cost Optimization Strategies for Cloud Infrastructure: Azure & GCP',
                'abstract': '''Comprehensive guide to optimizing cloud costs for production workloads on Azure and GCP. Learn strategies for right-sizing compute resources, using reserved capacity (34% savings on PostgreSQL), implementing auto-scaling to match demand, and lifecycle management for storage (Hot → Cool → Archive). Real-world case studies show reducing Azure infrastructure costs from $1,157/month to $721/month (38% reduction) through Application Insights sampling, blob lifecycle policies, and Redis optimization. Covers GCP cost optimization with preemptible nodes (70% savings), Cloud Storage vs Filestore trade-offs, and monitoring budgets with alerts. Includes detailed cost breakdowns, ROI calculations, and migration paths to Kubernetes for 35% additional savings.''',
                'authors': 'Vasu Kapoor',
                'source': 'arxiv',
                'source_id': 'vasu-cloud-cost-optimization-2024',
                'url': 'https://vasukapoor.com/blog/cloud-cost-optimization',
                'published_date': (datetime.now() - timedelta(days=14)).date(),
                'category': 'mlops',
                'tags': ['Cost Optimization', 'Azure', 'GCP', 'Cloud Economics', 'FinOps'],
                'citation_count': 52,
                'relevance_score': 0.86,
                'is_featured': False
            },
            {
                'title': 'Monitoring and Observability for Production Kubernetes Applications',
                'abstract': '''Essential guide to implementing monitoring and observability for Kubernetes workloads in production. Learn how to configure Prometheus for metrics collection, design Grafana dashboards for visualization, implement custom metrics (request latency, queue depth), and set up AlertManager for PagerDuty integration. Covers distributed tracing with OpenTelemetry, structured logging with Fluentd, and Azure Application Insights integration. Real-world examples show monitoring a multi-component system (Django, Celery, PostgreSQL, Redis) with SLI/SLO definitions, p95/p99 latency tracking, and automated incident response. Includes YAML configurations for ServiceMonitor, PrometheusRule, and log aggregation pipelines. Critical for platform engineers ensuring reliability at scale.''',
                'authors': 'Vasu Kapoor',
                'source': 'paperswithcode',
                'source_id': 'vasu-k8s-monitoring-observability-2024',
                'url': 'https://vasukapoor.com/blog/kubernetes-monitoring-observability',
                'published_date': (datetime.now() - timedelta(days=11)).date(),
                'category': 'mlops',
                'tags': ['Monitoring', 'Observability', 'Prometheus', 'Grafana', 'Kubernetes', 'SRE'],
                'citation_count': 43,
                'relevance_score': 0.89,
                'is_featured': False
            },
            {
                'title': 'Zero-Downtime Deployments: Strategies for Production Kubernetes',
                'abstract': '''Master zero-downtime deployment strategies for production Kubernetes applications. Learn how to configure rolling updates (maxSurge, maxUnavailable), implement readiness and liveness probes, design pre-stop hooks for graceful shutdown, and handle database migrations with init containers. Real-world example shows deploying updates to a 3-pod Django application while maintaining 100% availability, preventing race conditions in migrations, and using pod disruption budgets for cluster maintenance. Covers blue-green deployments, canary releases with traffic splitting, automated rollbacks on health check failures, and testing strategies. Includes complete Kubernetes manifests and CI/CD pipeline configurations for GitOps workflows with ArgoCD.''',
                'authors': 'Vasu Kapoor',
                'source': 'huggingface',
                'source_id': 'vasu-zero-downtime-k8s-deployments-2024',
                'url': 'https://vasukapoor.com/blog/zero-downtime-kubernetes-deployments',
                'published_date': (datetime.now() - timedelta(days=6)).date(),
                'category': 'mlops',
                'tags': ['Kubernetes', 'Deployments', 'Zero Downtime', 'CI/CD', 'Reliability'],
                'citation_count': 61,
                'relevance_score': 0.93,
                'is_featured': True
            }
        ]

        created_count = 0
        for post_data in blog_posts:
            try:
                post = Paper.objects.create(**post_data)
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {post.title[:60]}...'))
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to create post: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Successfully created {created_count} blog posts!'))
        self.stdout.write(self.style.SUCCESS(f'Total posts in database: {Paper.objects.count()}'))
