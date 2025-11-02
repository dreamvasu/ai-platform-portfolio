import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function CaseStudies() {
  const [selectedCase, setSelectedCase] = useState('calibra');
  const [activeTab, setActiveTab] = useState('overview');

  const caseStudies = {
    calibra: {
      title: "Calibra - Enterprise Calibration Management Platform",
      role: "Lead Backend Architect & Platform Engineer",
      duration: "March 2024 - October 2024",
      industry: "Scientific Instrumentation & Calibration Services",
      deployment: "Azure App Service (Production)",
      category: "Production Systems",

      impact: [
        { metric: "10,000+", description: "Calibration requests annually" },
        { metric: "40%", description: "Reduced turnaround time" },
        { metric: "200+", description: "Hours/month saved" },
        { metric: "99.9%", description: "Uptime SLA" }
      ],

      techStack: [
        { name: "Django 4.2", color: "green" },
        { name: "PostgreSQL", color: "blue" },
        { name: "Redis", color: "red" },
        { name: "Celery", color: "emerald" },
        { name: "Docker", color: "cyan" },
        { name: "Azure", color: "blue" },
        { name: "Terraform", color: "purple" },
        { name: "GitLab CI/CD", color: "orange" }
      ],

      challenges: [
        {
          title: "Multi-Tenant Architecture",
          problem: "Complete data isolation for 20+ clients with custom branding and workflows",
          solution: "Implemented django-tenants with PostgreSQL schema-based isolation",
          result: "Zero cross-tenant data leakage, dynamic provisioning, tenant-aware backups"
        },
        {
          title: "High-Volume PDF Generation",
          problem: "500+ calibration certificates daily, initial 30s blocking generation time",
          solution: "Async PDF generation with Celery distributed workers and caching",
          result: "Reduced to 3-5s, 95% cache hit rate, zero timeout errors"
        },
        {
          title: "Database Performance",
          problem: "Complex queries with 15+ joins causing 5-10s page loads",
          solution: "Query optimization with select_related, prefetch_related, strategic indexes",
          result: "200-400ms query time, 60% CPU reduction, supports 1000+ concurrent users"
        },
        {
          title: "Zero-Downtime Migrations",
          problem: "50GB+ data across 20 tenants, traditional migrations locked tables 10+ minutes",
          solution: "Blue-green migration strategy with tenant-specific rollout",
          result: "Zero downtime, failed migrations caught before rollout"
        }
      ],

      metrics: {
        performance: [
          { label: "API Response Time (p50)", value: "120ms" },
          { label: "API Response Time (p95)", value: "450ms" },
          { label: "PDF Generation Time", value: "3-5s" },
          { label: "Database Query Time", value: "35ms" },
          { label: "Concurrent Users", value: "1000+" },
          { label: "Daily API Requests", value: "500K+" }
        ],
        scale: [
          { label: "Active Tenants", value: "20" },
          { label: "Total Users", value: "800+" },
          { label: "SRFs/Year", value: "10,000+" },
          { label: "Database Size", value: "85GB" },
          { label: "Blob Storage", value: "50GB" },
          { label: "Uptime (6 months)", value: "99.94%" }
        ],
        code: [
          { label: "Test Coverage", value: "87%" },
          { label: "Lines of Code", value: "45,000+" },
          { label: "API Endpoints", value: "120+" },
          { label: "Database Tables", value: "80+" },
          { label: "Celery Tasks", value: "25" }
        ]
      }
    },

    ringlet: {
      title: "Ringlet - Educational Platform on Kubernetes",
      role: "Platform Engineer & DevOps Architect",
      duration: "November 2024",
      industry: "Educational Technology & E-Learning",
      deployment: "Kubernetes (GKE-Ready)",
      category: "Platform Engineering",

      impact: [
        { metric: "3-10", description: "Auto-scaling pods" },
        { metric: "60%", description: "Image size reduction" },
        { metric: "< 200ms", description: "Average response time" },
        { metric: "99.9%", description: "Target availability" }
      ],

      techStack: [
        { name: "Django 4.x", color: "green" },
        { name: "PostgreSQL 15", color: "blue" },
        { name: "Redis 7", color: "red" },
        { name: "Celery", color: "emerald" },
        { name: "Kubernetes", color: "blue" },
        { name: "Docker", color: "cyan" },
        { name: "Helm 3", color: "purple" },
        { name: "GKE", color: "blue" }
      ],

      challenges: [
        {
          title: "Container Optimization",
          problem: "Large Docker images increasing deployment time and storage costs",
          solution: "Multi-stage Docker builds separating build and runtime dependencies",
          result: "60% image size reduction, faster deployments, reduced storage costs"
        },
        {
          title: "Database Migrations in K8s",
          problem: "Race conditions during rolling updates when multiple pods run migrations",
          solution: "Init containers with single-run migrations before pod startup",
          result: "Clean separation of concerns, no race conditions, zero failed migrations"
        },
        {
          title: "Shared Media Storage",
          problem: "Multiple pods need read-write access to educational content (videos, PDFs)",
          solution: "ReadWriteMany PVCs using GKE Filestore for shared volume access",
          result: "All pods access same media files, consistent user experience"
        },
        {
          title: "Celery Beat Singleton",
          problem: "Multiple Celery Beat schedulers creating duplicate scheduled tasks",
          solution: "Single-replica deployment for beat, separate from scalable workers",
          result: "No duplicate tasks, clean scheduler separation"
        }
      ],

      metrics: {
        performance: [
          { label: "Response Time (p50)", value: "< 200ms" },
          { label: "Response Time (p95)", value: "< 500ms" },
          { label: "Pod Startup Time", value: "< 30s" },
          { label: "Scale-up Time", value: "< 60s" },
          { label: "Throughput", value: "1000+ req/s" },
          { label: "Resource Efficiency", value: "60-70% CPU" }
        ],
        scale: [
          { label: "Min Replicas", value: "3" },
          { label: "Max Replicas", value: "10" },
          { label: "Celery Workers", value: "2-6" },
          { label: "DB Storage", value: "10Gi" },
          { label: "Media Storage", value: "20Gi" },
          { label: "Target Uptime", value: "99.9%" }
        ],
        code: [
          { label: "K8s Manifests", value: "9 files" },
          { label: "Helm Chart", value: "Complete" },
          { label: "Docker Layers", value: "Multi-stage" },
          { label: "Health Checks", value: "Liveness + Readiness" },
          { label: "HPA Enabled", value: "Yes" }
        ]
      }
    }
  };

  const caseStudy = caseStudies[selectedCase];

  const getColorClass = (color) => {
    const colors = {
      blue: 'bg-blue-100 text-blue-700',
      green: 'bg-green-100 text-green-700',
      purple: 'bg-purple-100 text-purple-700',
      orange: 'bg-orange-100 text-orange-700',
      red: 'bg-red-100 text-red-700',
      cyan: 'bg-cyan-100 text-cyan-700',
      emerald: 'bg-emerald-100 text-emerald-700',
    };
    return colors[color] || 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Case Study Selector */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex gap-4">
            <button
              onClick={() => { setSelectedCase('calibra'); setActiveTab('overview'); }}
              className={`px-6 py-3 rounded-lg font-medium transition-all ${
                selectedCase === 'calibra'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <div className="text-left">
                <div className="font-bold">Calibra</div>
                <div className="text-xs opacity-80">Production Systems</div>
              </div>
            </button>
            <button
              onClick={() => { setSelectedCase('ringlet'); setActiveTab('overview'); }}
              className={`px-6 py-3 rounded-lg font-medium transition-all ${
                selectedCase === 'ringlet'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <div className="text-left">
                <div className="font-bold">Ringlet</div>
                <div className="text-xs opacity-80">Platform Engineering</div>
              </div>
            </button>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-gray-900 to-gray-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h1 className="text-5xl font-bold mb-4">{caseStudy.title}</h1>
            <p className="text-xl text-gray-300 mb-6">
              {caseStudy.role} | {caseStudy.duration}
            </p>
            <div className="flex justify-center gap-4 text-sm">
              <span className="bg-blue-600 px-4 py-2 rounded-full">{caseStudy.industry}</span>
              <span className="bg-green-600 px-4 py-2 rounded-full">{caseStudy.deployment}</span>
            </div>
          </div>

          {/* Impact Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-12">
            {caseStudy.impact.map((item, idx) => (
              <div key={idx} className="bg-white/10 backdrop-blur-sm rounded-lg p-6 text-center">
                <div className="text-4xl font-bold text-blue-400 mb-2">{item.metric}</div>
                <div className="text-sm text-gray-300">{item.description}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tab Navigation */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8 overflow-x-auto">
            {['overview', 'challenges', 'architecture', 'metrics'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-2 border-b-2 font-medium text-sm capitalize whitespace-nowrap ${
                  activeTab === tab
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content Sections */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-3xl font-bold mb-6">Executive Summary</h2>
              <p className="text-lg text-gray-700 mb-6">
                Calibra is a multi-tenant SaaS platform managing end-to-end calibration workflows for
                scientific instrumentation companies. The platform handles service request forms (SRFs),
                equipment observations, calibration certificates, and quotation management with complex
                scientific calculations and regulatory compliance requirements.
              </p>

              <h3 className="text-2xl font-bold mb-4 mt-8">Tech Stack</h3>
              <div className="flex flex-wrap gap-3">
                {caseStudy.techStack.map((tech, idx) => (
                  <span
                    key={idx}
                    className={`px-4 py-2 rounded-lg font-medium ${getColorClass(tech.color)}`}
                  >
                    {tech.name}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-3xl font-bold mb-6">Key Achievements</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="border-l-4 border-blue-500 pl-4">
                  <h4 className="font-bold text-lg mb-2">Multi-Tenant Architecture</h4>
                  <p className="text-gray-600">
                    Complete data isolation with PostgreSQL schema-based isolation for 20+ clients
                  </p>
                </div>
                <div className="border-l-4 border-green-500 pl-4">
                  <h4 className="font-bold text-lg mb-2">Event Sourcing</h4>
                  <p className="text-gray-600">
                    Immutable record-keeping with full audit trail for ISO 17025 compliance
                  </p>
                </div>
                <div className="border-l-4 border-purple-500 pl-4">
                  <h4 className="font-bold text-lg mb-2">Async Processing</h4>
                  <p className="text-gray-600">
                    Celery distributed workers handling 500+ PDFs daily with 95% cache hit rate
                  </p>
                </div>
                <div className="border-l-4 border-orange-500 pl-4">
                  <h4 className="font-bold text-lg mb-2">Infrastructure as Code</h4>
                  <p className="text-gray-600">
                    Terraform-managed Azure infrastructure with automated CI/CD pipelines
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Challenges Tab */}
        {activeTab === 'challenges' && (
          <div className="space-y-6">
            {caseStudy.challenges.map((challenge, idx) => (
              <div key={idx} className="bg-white rounded-lg shadow-lg p-8">
                <h3 className="text-2xl font-bold mb-4">{challenge.title}</h3>

                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold text-red-600 mb-2">Problem:</h4>
                    <p className="text-gray-700">{challenge.problem}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-blue-600 mb-2">Solution:</h4>
                    <p className="text-gray-700">{challenge.solution}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-green-600 mb-2">Result:</h4>
                    <p className="text-gray-700">{challenge.result}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Architecture Tab */}
        {activeTab === 'architecture' && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-3xl font-bold mb-6">System Architecture</h2>

            <div className="mb-8">
              <h3 className="text-xl font-bold mb-4">Multi-Tenancy Pattern</h3>
              <div className="bg-gray-900 text-green-400 p-6 rounded-lg font-mono text-sm overflow-x-auto">
                <pre>{`┌─────────────────────────────────────────────────┐
│          Shared Database (PostgreSQL)            │
├─────────────────────────────────────────────────┤
│  Schema: public        │ Core tenant registry   │
│  Schema: client_acme   │ Acme Corp's data       │
│  Schema: client_techco │ TechCo's data          │
│  Schema: client_labx   │ LabX's data            │
└─────────────────────────────────────────────────┘

Tenant Routing:
acme.calibra.com      → client_acme schema
techco.calibra.com    → client_techco schema
custom-domain.com     → mapped tenant schema`}</pre>
              </div>
            </div>

            <div className="mb-8">
              <h3 className="text-xl font-bold mb-4">Azure Architecture</h3>
              <div className="bg-gray-50 p-6 rounded-lg">
                <ul className="space-y-3">
                  <li className="flex items-start">
                    <span className="bg-blue-500 text-white px-3 py-1 rounded mr-3 text-sm font-medium">App Service</span>
                    <span className="text-gray-700">Django application with Gunicorn (4 workers, auto-scaling 2-10 instances)</span>
                  </li>
                  <li className="flex items-start">
                    <span className="bg-green-500 text-white px-3 py-1 rounded mr-3 text-sm font-medium">PostgreSQL</span>
                    <span className="text-gray-700">Flexible Server (Premium SSD, multi-tenant schemas)</span>
                  </li>
                  <li className="flex items-start">
                    <span className="bg-red-500 text-white px-3 py-1 rounded mr-3 text-sm font-medium">Redis Cache</span>
                    <span className="text-gray-700">6GB High Availability (session store + Celery broker)</span>
                  </li>
                  <li className="flex items-start">
                    <span className="bg-purple-500 text-white px-3 py-1 rounded mr-3 text-sm font-medium">Blob Storage</span>
                    <span className="text-gray-700">PDF reports (~50GB) with GRS replication</span>
                  </li>
                  <li className="flex items-start">
                    <span className="bg-orange-500 text-white px-3 py-1 rounded mr-3 text-sm font-medium">App Insights</span>
                    <span className="text-gray-700">Full observability with custom metrics and distributed tracing</span>
                  </li>
                </ul>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-bold mb-4">DevOps Pipeline</h3>
              <div className="bg-gray-50 p-6 rounded-lg">
                <div className="flex items-center justify-between mb-4 text-sm">
                  <span className="font-medium">GitLab Push</span>
                  <span>→</span>
                  <span className="font-medium">Run Tests</span>
                  <span>→</span>
                  <span className="font-medium">Build Docker</span>
                  <span>→</span>
                  <span className="font-medium">Deploy Staging</span>
                  <span>→</span>
                  <span className="font-medium">Manual Approval</span>
                  <span>→</span>
                  <span className="font-medium">Deploy Production</span>
                </div>
                <p className="text-gray-600 text-sm">
                  Fully automated CI/CD with Terraform infrastructure provisioning,
                  automated testing (87% coverage), and blue-green deployments
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Metrics Tab */}
        {activeTab === 'metrics' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-3xl font-bold mb-6">Performance Metrics</h2>
              <div className="grid md:grid-cols-3 gap-6">
                {caseStudy.metrics.performance.map((metric, idx) => (
                  <div key={idx} className="border-l-4 border-blue-500 pl-4">
                    <div className="text-2xl font-bold text-blue-600">{metric.value}</div>
                    <div className="text-sm text-gray-600">{metric.label}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-3xl font-bold mb-6">Scale Metrics</h2>
              <div className="grid md:grid-cols-3 gap-6">
                {caseStudy.metrics.scale.map((metric, idx) => (
                  <div key={idx} className="border-l-4 border-green-500 pl-4">
                    <div className="text-2xl font-bold text-green-600">{metric.value}</div>
                    <div className="text-sm text-gray-600">{metric.label}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-3xl font-bold mb-6">Code Quality Metrics</h2>
              <div className="grid md:grid-cols-3 gap-6">
                {caseStudy.metrics.code.map((metric, idx) => (
                  <div key={idx} className="border-l-4 border-purple-500 pl-4">
                    <div className="text-2xl font-bold text-purple-600">{metric.value}</div>
                    <div className="text-sm text-gray-600">{metric.label}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* CTA Section */}
      <section className="bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Want to know more?</h2>
          <p className="text-xl text-gray-300 mb-8">
            Ask the AI chatbot about {caseStudy.title.split(' - ')[0]}'s architecture, challenges, or any technical details
          </p>
          <div className="space-y-2 text-gray-400">
            {selectedCase === 'calibra' ? (
              <>
                <p>Try asking: "Tell me about Calibra's multi-tenant architecture"</p>
                <p>Or: "How did Vasu optimize the PDF generation?"</p>
              </>
            ) : (
              <>
                <p>Try asking: "Tell me about Ringlet's Kubernetes deployment"</p>
                <p>Or: "How did Vasu optimize Docker images for Ringlet?"</p>
              </>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
