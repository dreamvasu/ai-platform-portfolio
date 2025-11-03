import { useState } from 'react';
import { ChevronDown, ChevronRight, Copy, Check, Terminal, Code, Wrench } from 'lucide-react';

export default function TechSOPs() {
  const [expandedSection, setExpandedSection] = useState(null);
  const [copiedCode, setCopiedCode] = useState(null);

  const copyToClipboard = (code, id) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  const sops = [
    {
      id: 'kubernetes',
      title: 'Kubernetes Production Patterns',
      icon: '☸️',
      color: 'blue',
      guidelines: [
        {
          title: 'Zero-Downtime Deployments',
          type: 'deployment',
          description: 'Rolling updates with proper health checks',
          code: `apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-api
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      containers:
      - name: api
        image: gcr.io/project/ml-api:v2
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5`,
          commands: [
            'kubectl apply -f deployment.yaml',
            'kubectl rollout status deployment/ml-api',
            'kubectl rollout undo deployment/ml-api  # Instant rollback'
          ]
        },
        {
          title: 'Production-Ready Service Mesh',
          type: 'networking',
          description: 'Expose ML models with load balancing',
          code: `apiVersion: v1
kind: Service
metadata:
  name: ml-api-service
  annotations:
    cloud.google.com/neg: '{"ingress": true}'
spec:
  type: LoadBalancer
  selector:
    app: ml-api
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  sessionAffinity: ClientIP`,
          commands: [
            'kubectl get svc ml-api-service  # Get external IP',
            'kubectl describe svc ml-api-service',
            'kubectl logs -l app=ml-api --tail=100 -f'
          ]
        },
        {
          title: 'Auto-Scaling ML Workloads',
          type: 'autoscaling',
          description: 'HPA for traffic spikes',
          code: `apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80`,
          commands: [
            'kubectl get hpa',
            'kubectl describe hpa ml-api-hpa',
            'kubectl top pods  # Monitor resource usage'
          ]
        }
      ]
    },
    {
      id: 'gcp',
      title: 'GCP Production Infrastructure',
      icon: '☁️',
      color: 'red',
      guidelines: [
        {
          title: 'Cloud Run with Cloud SQL',
          type: 'deployment',
          description: 'Serverless Django with managed PostgreSQL',
          code: `# Deploy with Unix socket connection
gcloud run deploy api \\
  --source . \\
  --region=us-central1 \\
  --platform=managed \\
  --allow-unauthenticated \\
  --add-cloudsql-instances=PROJECT:REGION:INSTANCE \\
  --update-env-vars="DATABASE_URL=postgresql://user:pass@/db?host=/cloudsql/PROJECT:REGION:INSTANCE" \\
  --set-secrets="SECRET_KEY=DJANGO_SECRET:latest" \\
  --memory=2Gi \\
  --cpu=2 \\
  --min-instances=1 \\
  --max-instances=100 \\
  --concurrency=80`,
          commands: [
            'gcloud run services list',
            'gcloud run services describe api --region=us-central1',
            'gcloud logging read "resource.type=cloud_run_revision" --limit=50'
          ]
        },
        {
          title: 'Secret Manager Best Practices',
          type: 'security',
          description: 'Never commit secrets - use Secret Manager',
          code: `# Create secret
echo -n "your-secret-key" | gcloud secrets create DJANGO_SECRET --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding DJANGO_SECRET \\
  --member="serviceAccount:PROJECT-NUMBER-compute@developer.gserviceaccount.com" \\
  --role="roles/secretmanager.secretAccessor"

# Access in Cloud Run
gcloud run services update api \\
  --set-secrets="SECRET_KEY=DJANGO_SECRET:latest"`,
          commands: [
            'gcloud secrets list',
            'gcloud secrets versions access latest --secret="DJANGO_SECRET"',
            'gcloud secrets add-iam-policy-binding DJANGO_SECRET --member="user:you@example.com" --role="roles/secretmanager.secretAccessor"'
          ]
        },
        {
          title: 'Load Balancer + Cloud CDN',
          type: 'networking',
          description: 'Global HTTP(S) load balancing with caching',
          code: `# Create backend bucket for static assets
gcloud compute backend-buckets create static-assets \\
  --gcs-bucket-name=your-static-bucket \\
  --enable-cdn

# Create URL map
gcloud compute url-maps create app-lb \\
  --default-service=api-backend-service

# Add SSL certificate
gcloud compute ssl-certificates create app-cert \\
  --domains=yourdomain.com

# Create HTTPS proxy
gcloud compute target-https-proxies create app-https-proxy \\
  --url-map=app-lb \\
  --ssl-certificates=app-cert`,
          commands: [
            'gcloud compute backend-services list',
            'gcloud compute url-maps describe app-lb',
            'gcloud compute forwarding-rules list'
          ]
        }
      ]
    },
    {
      id: 'django',
      title: 'Django Production Optimization',
      icon: '🐍',
      color: 'green',
      guidelines: [
        {
          title: 'Production Settings',
          type: 'config',
          description: 'Security-hardened Django configuration',
          code: `# settings/production.py
import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Database connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000'
        },
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}

# Caching with Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
        }
    }
}`,
          commands: [
            'python manage.py check --deploy',
            'python manage.py migrate --noinput',
            'gunicorn --bind :$PORT --workers 4 --threads 2 --timeout 300 core.wsgi:application'
          ]
        },
        {
          title: 'Database Query Optimization',
          type: 'performance',
          description: 'N+1 query prevention and indexing',
          code: `# BAD - N+1 queries
projects = Project.objects.all()
for project in projects:
    print(project.tech_stack.all())  # Query for each project!

# GOOD - Prefetch related
projects = Project.objects.prefetch_related('tech_stack').all()
for project in projects:
    print(project.tech_stack.all())  # Already loaded!

# GOOD - Select related for ForeignKey
papers = Paper.objects.select_related('category').all()

# Add database indexes
class Meta:
    indexes = [
        models.Index(fields=['published_date', '-relevance_score']),
        models.Index(fields=['category', 'is_featured']),
    ]`,
          commands: [
            'python manage.py makemigrations',
            'python manage.py sqlmigrate portfolio 0001  # See actual SQL',
            'python manage.py shell_plus --print-sql  # Debug queries'
          ]
        },
        {
          title: 'API Rate Limiting',
          type: 'security',
          description: 'Throttle requests to prevent abuse',
          code: `# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# Custom throttle for specific views
from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    rate = '60/min'

class SustainedRateThrottle(UserRateThrottle):
    rate = '1000/day'

class PaperViewSet(viewsets.ModelViewSet):
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]`,
          commands: [
            'python manage.py test',
            'locust -f locustfile.py --host=http://localhost:8000',
            'hey -n 1000 -c 10 http://localhost:8000/api/papers/'
          ]
        }
      ]
    },
    {
      id: 'mlops',
      title: 'MLOps Production Patterns',
      icon: '🤖',
      color: 'purple',
      guidelines: [
        {
          title: 'Model Serving with FastAPI',
          type: 'deployment',
          description: 'High-performance model inference API',
          code: `from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import torch
from functools import lru_cache

app = FastAPI()

@lru_cache()
def load_model():
    """Load model once and cache"""
    model = torch.load('model.pth')
    model.eval()
    return model

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    latency_ms: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    import time
    start = time.time()

    model = load_model()
    features = torch.tensor([request.features])

    with torch.no_grad():
        output = model(features)
        prediction = output.item()
        confidence = torch.softmax(output, dim=1).max().item()

    latency = (time.time() - start) * 1000

    return PredictionResponse(
        prediction=prediction,
        confidence=confidence,
        latency_ms=round(latency, 2)
    )

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": load_model() is not None}`,
          commands: [
            'uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4',
            'docker build -t ml-api .',
            'docker run -p 8000:8000 ml-api'
          ]
        },
        {
          title: 'Model Monitoring & Drift Detection',
          type: 'monitoring',
          description: 'Track model performance in production',
          code: `import prometheus_client as prom
from datetime import datetime

# Metrics
prediction_latency = prom.Histogram(
    'model_prediction_latency_seconds',
    'Model prediction latency',
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

prediction_counter = prom.Counter(
    'model_predictions_total',
    'Total predictions',
    ['model_version', 'status']
)

confidence_gauge = prom.Gauge(
    'model_confidence',
    'Model prediction confidence'
)

@app.post("/predict")
async def predict(request: PredictionRequest):
    with prediction_latency.time():
        try:
            result = await run_inference(request)
            prediction_counter.labels(
                model_version='v2.1',
                status='success'
            ).inc()
            confidence_gauge.set(result.confidence)
            return result
        except Exception as e:
            prediction_counter.labels(
                model_version='v2.1',
                status='error'
            ).inc()
            raise

# Expose metrics
@app.get("/metrics")
async def metrics():
    return prom.generate_latest()`,
          commands: [
            'curl http://localhost:8000/metrics',
            'kubectl apply -f prometheus-config.yaml',
            'kubectl port-forward svc/prometheus 9090:9090'
          ]
        }
      ]
    },
    {
      id: 'react',
      title: 'React Production Optimization',
      icon: '⚛️',
      color: 'cyan',
      guidelines: [
        {
          title: 'Code Splitting & Lazy Loading',
          type: 'performance',
          description: 'Reduce initial bundle size',
          code: `import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Lazy load heavy components
const CaseStudies = lazy(() => import('./pages/CaseStudies'));
const TechSOPs = lazy(() => import('./pages/TechSOPs'));
const Kubernetes = lazy(() => import('./pages/Kubernetes'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={
        <div className="flex items-center justify-center h-screen">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
        </div>
      }>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/case-studies" element={<CaseStudies />} />
          <Route path="/tech-sops" element={<TechSOPs />} />
          <Route path="/kubernetes" element={<Kubernetes />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}`,
          commands: [
            'npm run build',
            'npx vite-bundle-visualizer',
            'npm run preview'
          ]
        },
        {
          title: 'API Call Optimization',
          type: 'performance',
          description: 'Prevent unnecessary re-fetches',
          code: `import { useQuery } from '@tanstack/react-query';
import { getTechStack } from './api';

function TechStackSection() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['techStack'],
    queryFn: getTechStack,
    staleTime: 5 * 60 * 1000,  // 5 minutes
    cacheTime: 30 * 60 * 1000,  // 30 minutes
    refetchOnWindowFocus: false,
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div className="grid grid-cols-3 gap-4">
      {data.results.map(tech => (
        <TechCard key={tech.id} tech={tech} />
      ))}
    </div>
  );
}`,
          commands: [
            'npm install @tanstack/react-query',
            'npm run dev',
            'npm run build -- --analyze'
          ]
        }
      ]
    },
    {
      id: 'terraform',
      title: 'Infrastructure as Code',
      icon: '🏗️',
      color: 'purple',
      guidelines: [
        {
          title: 'GCP Project Setup with Terraform',
          type: 'infrastructure',
          description: 'Reproducible cloud infrastructure',
          code: `# main.tf
terraform {
  required_version = ">= 1.0"
  backend "gcs" {
    bucket = "tfstate-bucket"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Cloud Run service
resource "google_cloud_run_service" "api" {
  name     = "portfolio-api"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/\${var.project_id}/api:latest"

        resources {
          limits = {
            cpu    = "2000m"
            memory = "2Gi"
          }
        }

        env {
          name  = "DATABASE_URL"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.db_url.secret_id
              key  = "latest"
            }
          }
        }
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "100"
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.main.connection_name
      }
    }
  }
}

# Cloud SQL
resource "google_sql_database_instance" "main" {
  name             = "portfolio-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"

    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }

    ip_configuration {
      ipv4_enabled = false
      require_ssl  = true
    }
  }
}`,
          commands: [
            'terraform init',
            'terraform plan -out=tfplan',
            'terraform apply tfplan',
            'terraform destroy  # Cleanup'
          ]
        }
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      {/* Hero */}
      <section className="bg-gradient-to-r from-gray-900 to-gray-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3 mb-4">
            <Terminal className="w-10 h-10" />
            <h1 className="text-5xl font-bold">Technical SOPs & Guidelines</h1>
          </div>
          <p className="text-xl text-gray-300 max-w-4xl">
            Production-ready code snippets, configurations, and best practices.
            Copy-paste solutions from real-world deployments - no theory, just hands-on patterns that work.
          </p>
          <div className="mt-8 flex items-center gap-6">
            <div className="flex items-center gap-2">
              <Code className="w-5 h-5 text-blue-400" />
              <span className="text-sm">Ready-to-use code</span>
            </div>
            <div className="flex items-center gap-2">
              <Wrench className="w-5 h-5 text-green-400" />
              <span className="text-sm">Production tested</span>
            </div>
            <div className="flex items-center gap-2">
              <Terminal className="w-5 h-5 text-purple-400" />
              <span className="text-sm">Real commands</span>
            </div>
          </div>
        </div>
      </section>

      {/* SOPs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="space-y-6">
          {sops.map((section) => (
            <div key={section.id} className="bg-white rounded-lg shadow-lg overflow-hidden border border-gray-200">
              {/* Section Header */}
              <button
                onClick={() => setExpandedSection(expandedSection === section.id ? null : section.id)}
                className="w-full flex items-center justify-between p-6 hover:bg-gray-50 transition"
              >
                <div className="flex items-center gap-4">
                  <span className="text-4xl">{section.icon}</span>
                  <div className="text-left">
                    <h2 className="text-2xl font-bold text-gray-900">{section.title}</h2>
                    <p className="text-sm text-gray-600 mt-1">{section.guidelines.length} production patterns</p>
                  </div>
                </div>
                {expandedSection === section.id ? (
                  <ChevronDown className="w-6 h-6 text-gray-600" />
                ) : (
                  <ChevronRight className="w-6 h-6 text-gray-600" />
                )}
              </button>

              {/* Section Content */}
              {expandedSection === section.id && (
                <div className="border-t border-gray-200 bg-gray-50">
                  {section.guidelines.map((guideline, idx) => (
                    <div key={idx} className="p-6 border-b border-gray-200 last:border-b-0">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="text-xl font-bold text-gray-900 mb-2">{guideline.title}</h3>
                          <p className="text-gray-600">{guideline.description}</p>
                          <span className={`inline-block mt-2 px-3 py-1 rounded-full text-xs font-medium bg-${section.color}-100 text-${section.color}-700`}>
                            {guideline.type}
                          </span>
                        </div>
                      </div>

                      {/* Code Block */}
                      <div className="bg-gray-900 rounded-lg p-4 mb-4 relative group">
                        <button
                          onClick={() => copyToClipboard(guideline.code, `${section.id}-${idx}`)}
                          className="absolute top-4 right-4 p-2 rounded bg-gray-800 hover:bg-gray-700 transition opacity-0 group-hover:opacity-100"
                        >
                          {copiedCode === `${section.id}-${idx}` ? (
                            <Check className="w-4 h-4 text-green-400" />
                          ) : (
                            <Copy className="w-4 h-4 text-gray-400" />
                          )}
                        </button>
                        <pre className="text-sm text-gray-100 overflow-x-auto">
                          <code>{guideline.code}</code>
                        </pre>
                      </div>

                      {/* Commands */}
                      {guideline.commands && guideline.commands.length > 0 && (
                        <div>
                          <h4 className="text-sm font-bold text-gray-700 mb-2 flex items-center gap-2">
                            <Terminal className="w-4 h-4" />
                            Quick Commands
                          </h4>
                          <div className="space-y-2">
                            {guideline.commands.map((cmd, cmdIdx) => (
                              <div key={cmdIdx} className="flex items-center gap-2 bg-gray-100 rounded p-3 group hover:bg-gray-200 transition">
                                <code className="flex-1 text-sm font-mono text-gray-800">{cmd}</code>
                                <button
                                  onClick={() => copyToClipboard(cmd, `${section.id}-${idx}-cmd-${cmdIdx}`)}
                                  className="p-1 rounded hover:bg-gray-300 transition opacity-0 group-hover:opacity-100"
                                >
                                  {copiedCode === `${section.id}-${idx}-cmd-${cmdIdx}` ? (
                                    <Check className="w-4 h-4 text-green-600" />
                                  ) : (
                                    <Copy className="w-4 h-4 text-gray-600" />
                                  )}
                                </button>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Footer CTA */}
        <div className="mt-12 bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-8 text-white text-center">
          <h3 className="text-2xl font-bold mb-4">Need Custom Solutions?</h3>
          <p className="text-blue-100 mb-6">
            These patterns are from real production systems. Looking for architecture consulting or implementation help?
          </p>
          <a
            href="/case-studies"
            className="inline-block bg-white text-blue-600 font-bold py-3 px-8 rounded-lg hover:bg-blue-50 transition"
          >
            View Production Case Studies →
          </a>
        </div>
      </div>
    </div>
  );
}
