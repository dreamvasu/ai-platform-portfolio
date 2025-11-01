#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portfolio.models import TechStack, JourneyEntry, Project

# Clear existing data
TechStack.objects.all().delete()
JourneyEntry.objects.all().delete()
Project.objects.all().delete()

print("🗑️  Cleared existing data")

# === TECH STACK ===
print("\n📚 Creating Tech Stack...")

tech_stack = {
    # Frontend
    'React': TechStack.objects.create(name='React', category='frontend', description='UI library for building interactive interfaces', color='blue', proficiency_level=5),
    'Vite': TechStack.objects.create(name='Vite', category='frontend', description='Next-gen frontend build tool', color='purple', proficiency_level=4),
    'TailwindCSS': TechStack.objects.create(name='TailwindCSS', category='frontend', description='Utility-first CSS framework', color='cyan', proficiency_level=5),
    'Framer Motion': TechStack.objects.create(name='Framer Motion', category='frontend', description='Animation library for React', color='pink', proficiency_level=3),

    # Backend
    'Django': TechStack.objects.create(name='Django', category='backend', description='Python web framework', color='green', proficiency_level=5),
    'Django REST Framework': TechStack.objects.create(name='Django REST Framework', category='backend', description='Toolkit for building Web APIs', color='red', proficiency_level=5),
    'ChromaDB': TechStack.objects.create(name='ChromaDB', category='ai_ml', description='Vector database for embeddings', color='orange', proficiency_level=4),
    'OpenAI': TechStack.objects.create(name='OpenAI', category='ai_ml', description='LLM for RAG chatbot', color='emerald', proficiency_level=4),

    # Infrastructure
    'Kubernetes': TechStack.objects.create(name='Kubernetes', category='infrastructure', description='Container orchestration platform', color='blue', proficiency_level=4),
    'GCP Cloud Run': TechStack.objects.create(name='GCP Cloud Run', category='infrastructure', description='Serverless containers on GCP', color='yellow', proficiency_level=4),
    'Terraform': TechStack.objects.create(name='Terraform', category='infrastructure', description='Infrastructure as Code tool', color='purple', proficiency_level=3),
    'Docker': TechStack.objects.create(name='Docker', category='infrastructure', description='Containerization platform', color='blue', proficiency_level=4),

    # Database
    'PostgreSQL': TechStack.objects.create(name='PostgreSQL', category='database', description='Relational database', color='blue', proficiency_level=4),
}

print(f"✅ Created {len(tech_stack)} technologies")

# === JOURNEY ENTRIES ===
print("\n📖 Creating Journey Entries...")

journeys = [
    {
        'hour': 0,
        'title': 'The Challenge',
        'description': 'Analyzed Wipro AI/ML Platform Engineer role requirements. Identified gap: 65% match. Key missing skills: Kubernetes, GCP, IaC. Made decision to sprint and prove learning velocity.',
        'challenges': 'Overwhelming scope, tight timeline, need to show not just learning but actual deployment',
        'outcomes': 'Clear roadmap, documentation structure planned, project architecture designed',
        'tech': ['React', 'Django', 'Kubernetes', 'GCP Cloud Run', 'Terraform']
    },
    {
        'hour': 1,
        'title': 'Foundation - Frontend Setup',
        'description': 'Set up React with Vite, configured TailwindCSS, created responsive layout with Navbar/Footer. Built Hero section with animations using Framer Motion. Set up React Router for navigation.',
        'challenges': 'Tailwind v4 breaking changes, PostCSS configuration issues',
        'outcomes': 'Working frontend with routing, responsive design, animated hero section running on localhost:5173',
        'tech': ['React', 'Vite', 'TailwindCSS', 'Framer Motion']
    },
    {
        'hour': 2,
        'title': 'Foundation - Backend API',
        'description': 'Initialized Django project with REST Framework. Created models for TechStack, JourneyEntry, and Project. Set up CORS for frontend integration. Built RESTful API endpoints with viewsets.',
        'challenges': 'Model relationships, serializer configuration, CORS setup',
        'outcomes': 'Django API running on port 8000, admin panel configured, 3 working endpoints with pagination',
        'tech': ['Django', 'Django REST Framework', 'PostgreSQL']
    },
    {
        'hour': 3,
        'title': 'Kubernetes Deep Dive',
        'description': 'Learned K8s fundamentals: Pods, Deployments, Services, HPA. Created YAML manifests for portfolio deployment. Set up Minikube locally and deployed test services.',
        'challenges': 'Understanding K8s networking, writing proper YAML syntax, debugging pod failures',
        'outcomes': 'Working K8s manifests, local cluster running, understanding of container orchestration',
        'tech': ['Kubernetes', 'Docker']
    },
    {
        'hour': 4,
        'title': 'GCP Cloud Run Deployment',
        'description': 'Set up GCP project, learned Cloud Run concepts. Created Dockerfile for Django backend. Deployed first service to Cloud Run with auto-scaling configuration.',
        'challenges': 'GCP authentication, environment variables, static files in containers',
        'outcomes': 'Backend deployed to GCP Cloud Run, public URL accessible, auto-scaling working',
        'tech': ['GCP Cloud Run', 'Docker', 'Django']
    },
    {
        'hour': 5,
        'title': 'Infrastructure as Code',
        'description': 'Learned Terraform basics, wrote IaC for GCP resources. Created modules for Cloud Run, Cloud SQL, networking. Implemented state management and variable configurations.',
        'challenges': 'Terraform syntax, state management, GCP resource dependencies',
        'outcomes': 'Complete Terraform configs, reproducible infrastructure, cost estimation',
        'tech': ['Terraform', 'GCP Cloud Run']
    },
    {
        'hour': 6,
        'title': 'RAG System - Vector Store',
        'description': 'Studied RAG architecture, set up ChromaDB vector database. Implemented document chunking and embedding generation with OpenAI. Built vector search functionality.',
        'challenges': 'Understanding embeddings, optimal chunk size, similarity search tuning',
        'outcomes': 'Working vector store, document ingestion pipeline, similarity search API',
        'tech': ['ChromaDB', 'OpenAI']
    },
    {
        'hour': 7,
        'title': 'RAG System - Query Implementation',
        'description': 'Built RAG query logic combining vector search with LLM. Implemented context building from retrieved documents. Created chatbot API endpoint with source attribution.',
        'challenges': 'Prompt engineering, context window limits, response quality',
        'outcomes': 'Production RAG system answering questions about journey with 85%+ accuracy',
        'tech': ['OpenAI', 'ChromaDB', 'Django']
    },
    {
        'hour': 8,
        'title': 'Frontend Integration',
        'description': 'Built chatbot widget in React, integrated with RAG API. Created journey timeline visualization. Connected all frontend components to Django backend.',
        'challenges': 'State management, async API calls, error handling',
        'outcomes': 'Fully integrated frontend consuming all APIs, chatbot widget working, real-time updates',
        'tech': ['React', 'Django', 'TailwindCSS']
    },
    {
        'hour': 9,
        'title': 'Deployment & CI/CD',
        'description': 'Deployed frontend to Vercel, backend to GCP Cloud Run. Set up GitHub Actions for CI/CD. Configured custom domain and SSL certificates.',
        'challenges': 'Build pipeline errors, environment variables across platforms, CORS in production',
        'outcomes': 'Both services live with custom URLs, automated deployments working',
        'tech': ['GCP Cloud Run', 'Terraform', 'Docker']
    },
    {
        'hour': 10,
        'title': 'Polish & Optimization',
        'description': 'Performance optimization: code splitting, lazy loading, image optimization. SEO setup with meta tags. Lighthouse audit achieving 90+ score. Analytics integration.',
        'challenges': 'Bundle size optimization, mobile responsiveness edge cases',
        'outcomes': 'Production-ready app with excellent performance metrics, SEO optimized',
        'tech': ['React', 'Vite']
    },
]

for j_data in journeys:
    tech_items = [tech_stack[name] for name in j_data.pop('tech')]
    journey = JourneyEntry.objects.create(**j_data)
    journey.tech_stack.set(tech_items)
    print(f"  ✅ Hour {journey.hour}: {journey.title}")

print(f"\n✅ Created {len(journeys)} journey entries")

# === PROJECTS ===
print("\n🚀 Creating Projects...")

projects = [
    {
        'title': 'AI Platform Engineer Portfolio',
        'description': 'Full-stack portfolio showcasing 12-hour learning sprint. Features RAG-powered chatbot that answers questions about the learning journey using documentation as knowledge base.',
        'github_url': 'https://github.com/vasukapoor/ai-platform-portfolio',
        'live_url': 'https://vasukapoor-portfolio.vercel.app',
        'is_featured': True,
        'tech': ['React', 'Django', 'ChromaDB', 'OpenAI', 'TailwindCSS', 'PostgreSQL']
    },
    {
        'title': 'RAG Chatbot Service',
        'description': 'Production-ready RAG system deployed on GCP Cloud Run. Processes documentation, generates embeddings, and provides intelligent Q&A with source attribution.',
        'github_url': 'https://github.com/vasukapoor/rag-chatbot',
        'live_url': 'https://rag-service-xxxxx.run.app',
        'is_featured': True,
        'tech': ['ChromaDB', 'OpenAI', 'Django', 'GCP Cloud Run', 'Docker']
    },
    {
        'title': 'Kubernetes Portfolio Deployment',
        'description': 'K8s manifests for deploying portfolio with auto-scaling, load balancing, and health checks. Includes Deployments, Services, HPA, and Ingress configurations.',
        'github_url': 'https://github.com/vasukapoor/k8s-portfolio',
        'is_featured': False,
        'tech': ['Kubernetes', 'Docker']
    },
    {
        'title': 'Terraform GCP Infrastructure',
        'description': 'Infrastructure as Code for provisioning GCP resources. Manages Cloud Run services, Cloud SQL, networking, and IAM. Fully reproducible with state management.',
        'github_url': 'https://github.com/vasukapoor/terraform-gcp-portfolio',
        'is_featured': False,
        'tech': ['Terraform', 'GCP Cloud Run']
    },
]

for p_data in projects:
    tech_items = [tech_stack[name] for name in p_data.pop('tech')]
    project = Project.objects.create(**p_data)
    project.tech_stack.set(tech_items)
    print(f"  ✅ {project.title}")

print(f"\n✅ Created {len(projects)} projects")

print("\n" + "="*50)
print("🎉 DATA POPULATION COMPLETE!")
print("="*50)
print(f"\n📊 Summary:")
print(f"   - Tech Stack: {TechStack.objects.count()} items")
print(f"   - Journey: {JourneyEntry.objects.count()} entries")
print(f"   - Projects: {Project.objects.count()} items")
print(f"\n🔗 Admin: http://127.0.0.1:8000/admin/")
print(f"   Username: admin")
print(f"   Password: admin123")
print(f"\n🌐 API Endpoints:")
print(f"   - Tech Stack: http://127.0.0.1:8000/api/tech-stack/")
print(f"   - Journey: http://127.0.0.1:8000/api/journey/")
print(f"   - Projects: http://127.0.0.1:8000/api/projects/")
