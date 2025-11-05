import { Shield, Activity, Database, Globe, AlertTriangle, CheckCircle, Clock, TrendingUp, Zap } from 'lucide-react';
import { useState } from 'react';

export default function HADR() {
  const [activeTab, setActiveTab] = useState('overview');

  const slaMetrics = {
    availability: '99.95%',
    rto: '15 min',
    rpo: '5 min',
    uptime: '99.94%'
  };

  const architectureComponents = [
    {
      name: 'Multi-Region Deployment',
      status: 'operational',
      regions: ['us-central1 (Primary)', 'us-east1 (Secondary)'],
      icon: Globe
    },
    {
      name: 'Database High Availability',
      status: 'operational',
      details: 'Regional HA + Read Replicas',
      icon: Database
    },
    {
      name: 'Automated Backups',
      status: 'operational',
      frequency: 'Daily at 3 AM UTC',
      icon: Shield
    },
    {
      name: 'Global Load Balancer',
      status: 'operational',
      latency: '< 100ms p50',
      icon: Zap
    }
  ];

  const drScenarios = [
    {
      scenario: 'Region Outage',
      rto: '15 minutes',
      rpo: '5 minutes',
      procedure: [
        'Automated DNS failover to secondary region',
        'Promote read replica to primary database',
        'Update application configuration',
        'Verify service health and data consistency',
        'Notify stakeholders of failover event'
      ]
    },
    {
      scenario: 'Database Corruption',
      rto: '1 hour',
      rpo: '15 minutes',
      procedure: [
        'Stop write traffic to prevent further corruption',
        'Identify corruption scope and affected tables',
        'Restore from latest automated backup',
        'Use point-in-time recovery if needed',
        'Validate data integrity with checksums',
        'Re-enable traffic and monitor closely'
      ]
    },
    {
      scenario: 'Complete Data Loss',
      rto: '4 hours',
      rpo: '24 hours',
      procedure: [
        'Create new Cloud SQL instance in alternate region',
        'Restore from multi-region backup in GCS',
        'Redeploy all Cloud Run services',
        'Restore vector embeddings and ML models',
        'Run end-to-end validation tests',
        'Gradual traffic migration with monitoring'
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-900 to-blue-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3 mb-4">
            <Shield className="w-12 h-12" />
            <h1 className="text-5xl font-bold">High Availability & Disaster Recovery</h1>
          </div>
          <p className="text-xl text-blue-100 max-w-3xl">
            Production-grade HA/DR architecture ensuring 99.9%+ uptime, &lt;15min RTO, and &lt;5min RPO
            for mission-critical AI/ML platform services.
          </p>

          {/* SLA Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <div className="text-3xl font-bold text-green-400">{slaMetrics.availability}</div>
              <div className="text-sm text-blue-200">Availability SLA</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <div className="text-3xl font-bold text-yellow-400">{slaMetrics.rto}</div>
              <div className="text-sm text-blue-200">Recovery Time</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <div className="text-3xl font-bold text-orange-400">{slaMetrics.rpo}</div>
              <div className="text-sm text-blue-200">Data Loss Window</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <div className="text-3xl font-bold text-purple-400">{slaMetrics.uptime}</div>
              <div className="text-sm text-blue-200">Current Uptime (30d)</div>
            </div>
          </div>
        </div>
      </section>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex gap-4 overflow-x-auto">
            {['overview', 'architecture', 'dr-procedures', 'sla-monitoring'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-4 font-medium whitespace-nowrap border-b-2 transition-colors ${
                  activeTab === tab
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                {tab.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Tab Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* System Status */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                <Activity className="w-8 h-8 text-green-600" />
                System Status & Health
              </h2>

              <div className="grid md:grid-cols-2 gap-6">
                {architectureComponents.map((component, idx) => {
                  const Icon = component.icon;
                  return (
                    <div key={idx} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <div className="p-2 bg-blue-100 rounded-lg">
                            <Icon className="w-6 h-6 text-blue-600" />
                          </div>
                          <div>
                            <h3 className="font-bold text-lg">{component.name}</h3>
                            <p className="text-sm text-gray-600">{component.details || component.frequency || component.latency}</p>
                          </div>
                        </div>
                        <span className="flex items-center gap-2 px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                          <CheckCircle className="w-4 h-4" />
                          {component.status}
                        </span>
                      </div>
                      {component.regions && (
                        <div className="mt-3 pt-3 border-t border-gray-100">
                          <p className="text-sm font-medium text-gray-700 mb-2">Deployed Regions:</p>
                          <div className="space-y-1">
                            {component.regions.map((region, i) => (
                              <div key={i} className="text-sm text-gray-600 flex items-center gap-2">
                                <Globe className="w-4 h-4" />
                                {region}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Key Features */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              <h2 className="text-3xl font-bold mb-6">HA/DR Capabilities</h2>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
                  <Shield className="w-12 h-12 text-blue-600 mx-auto mb-3" />
                  <h3 className="font-bold text-lg mb-2">Regional Redundancy</h3>
                  <p className="text-sm text-gray-700">Multi-region deployment with automatic failover</p>
                </div>
                <div className="text-center p-6 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
                  <Database className="w-12 h-12 text-green-600 mx-auto mb-3" />
                  <h3 className="font-bold text-lg mb-2">Data Protection</h3>
                  <p className="text-sm text-gray-700">Daily backups with 7-day point-in-time recovery</p>
                </div>
                <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg">
                  <TrendingUp className="w-12 h-12 text-purple-600 mx-auto mb-3" />
                  <h3 className="font-bold text-lg mb-2">Auto-Scaling</h3>
                  <p className="text-sm text-gray-700">1-100 instances with intelligent load balancing</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'architecture' && (
          <div className="space-y-8">
            {/* Architecture Diagram */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              <h2 className="text-3xl font-bold mb-6">Multi-Region Architecture</h2>

              <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg p-8 mb-6">
                <div className="grid md:grid-cols-2 gap-8">
                  {/* Primary Region */}
                  <div className="border-2 border-blue-500 rounded-lg p-6 bg-white">
                    <h3 className="font-bold text-xl mb-4 text-blue-600 flex items-center gap-2">
                      <Globe className="w-6 h-6" />
                      Primary Region (us-central1)
                    </h3>
                    <div className="space-y-3">
                      <div className="flex items-center gap-2 text-sm">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span>Cloud Run Backend (3 instances)</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span>Cloud SQL Primary (HA enabled)</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span>Paper Scraper Service</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span>Document Processor</span>
                      </div>
                    </div>
                  </div>

                  {/* Secondary Region */}
                  <div className="border-2 border-green-500 rounded-lg p-6 bg-white">
                    <h3 className="font-bold text-xl mb-4 text-green-600 flex items-center gap-2">
                      <Globe className="w-6 h-6" />
                      Secondary Region (us-east1)
                    </h3>
                    <div className="space-y-3">
                      <div className="flex items-center gap-2 text-sm">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span>Cloud Run Backend (standby)</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span>Cloud SQL Read Replica</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <Clock className="w-4 h-4 text-yellow-600" />
                        <span>Automatic Failover Target</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Global Components */}
                <div className="mt-6 border-2 border-purple-500 rounded-lg p-6 bg-white">
                  <h3 className="font-bold text-xl mb-4 text-purple-600">Global Components</h3>
                  <div className="grid md:grid-cols-3 gap-4">
                    <div className="text-sm">
                      <strong>Load Balancer:</strong> Global HTTP(S) LB with CDN
                    </div>
                    <div className="text-sm">
                      <strong>Storage:</strong> Multi-region Cloud Storage (us)
                    </div>
                    <div className="text-sm">
                      <strong>Monitoring:</strong> Uptime checks from 6 regions
                    </div>
                  </div>
                </div>
              </div>

              {/* Component Details */}
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-gray-50 rounded-lg p-6">
                  <h3 className="font-bold text-lg mb-3">Auto-Scaling Configuration</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Min Instances:</span>
                      <span className="font-medium">1 (always warm)</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Max Instances:</span>
                      <span className="font-medium">100</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Concurrency:</span>
                      <span className="font-medium">80 req/instance</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">CPU Threshold:</span>
                      <span className="font-medium">70%</span>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 rounded-lg p-6">
                  <h3 className="font-bold text-lg mb-3">Backup Strategy</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Frequency:</span>
                      <span className="font-medium">Daily at 3 AM UTC</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Automated Retention:</span>
                      <span className="font-medium">7 days</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Manual Retention:</span>
                      <span className="font-medium">30 days</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Location:</span>
                      <span className="font-medium">Multi-region (us)</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'dr-procedures' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                <AlertTriangle className="w-8 h-8 text-orange-600" />
                Disaster Recovery Runbooks
              </h2>

              {drScenarios.map((dr, idx) => (
                <div key={idx} className="mb-8 last:mb-0">
                  <div className="bg-gradient-to-r from-red-50 to-orange-50 border-l-4 border-red-500 rounded-r-lg p-6 mb-4">
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="font-bold text-xl text-gray-900">{dr.scenario}</h3>
                      <div className="flex gap-4">
                        <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs font-medium">
                          RTO: {dr.rto}
                        </span>
                        <span className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-xs font-medium">
                          RPO: {dr.rpo}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-gray-50 rounded-lg p-6">
                    <h4 className="font-bold mb-3 text-gray-700">Recovery Procedure:</h4>
                    <ol className="space-y-3">
                      {dr.procedure.map((step, stepIdx) => (
                        <li key={stepIdx} className="flex gap-3">
                          <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                            {stepIdx + 1}
                          </span>
                          <span className="text-gray-700">{step}</span>
                        </li>
                      ))}
                    </ol>
                  </div>
                </div>
              ))}
            </div>

            {/* DR Testing Schedule */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              <h2 className="text-2xl font-bold mb-6">Quarterly DR Drill Schedule</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="border border-gray-200 rounded-lg p-6">
                  <h3 className="font-bold mb-2">Q1: Region Failover Drill</h3>
                  <p className="text-sm text-gray-600">Switch traffic to secondary region, measure RTO/RPO, document lessons learned</p>
                </div>
                <div className="border border-gray-200 rounded-lg p-6">
                  <h3 className="font-bold mb-2">Q2: Database Restore Drill</h3>
                  <p className="text-sm text-gray-600">Full database restore to test environment, validate data integrity</p>
                </div>
                <div className="border border-gray-200 rounded-lg p-6">
                  <h3 className="font-bold mb-2">Q3: Full Stack Recovery Drill</h3>
                  <p className="text-sm text-gray-600">Simulate complete infrastructure loss, rebuild from backups</p>
                </div>
                <div className="border border-gray-200 rounded-lg p-6">
                  <h3 className="font-bold mb-2">Q4: Load & Chaos Test</h3>
                  <p className="text-sm text-gray-600">Inject random failures, measure system resilience, update runbooks</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'sla-monitoring' && (
          <div className="space-y-8">
            {/* SLA Targets */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              <h2 className="text-3xl font-bold mb-6">Service Level Agreements</h2>

              <div className="grid md:grid-cols-3 gap-6 mb-8">
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-6">
                  <h3 className="font-bold text-lg mb-2 text-green-800">Availability SLA</h3>
                  <div className="text-4xl font-bold text-green-600 mb-2">99.9%</div>
                  <p className="text-sm text-gray-700">43.2 min downtime/month allowed</p>
                </div>

                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-6">
                  <h3 className="font-bold text-lg mb-2 text-blue-800">Response Time SLA</h3>
                  <div className="text-4xl font-bold text-blue-600 mb-2">p95 &lt; 500ms</div>
                  <p className="text-sm text-gray-700">95% of requests under 500ms</p>
                </div>

                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-6">
                  <h3 className="font-bold text-lg mb-2 text-purple-800">Error Rate SLA</h3>
                  <div className="text-4xl font-bold text-purple-600 mb-2">&lt; 0.1%</div>
                  <p className="text-sm text-gray-700">99.9% success rate minimum</p>
                </div>
              </div>

              {/* Performance Metrics */}
              <div className="border border-gray-200 rounded-lg p-6">
                <h3 className="font-bold text-xl mb-4">Current Performance Metrics (24h)</h3>
                <div className="grid md:grid-cols-4 gap-6">
                  <div>
                    <div className="text-sm text-gray-600 mb-1">p50 Latency</div>
                    <div className="text-2xl font-bold text-green-600">87ms</div>
                    <div className="text-xs text-green-600">✓ Within SLA</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 mb-1">p95 Latency</div>
                    <div className="text-2xl font-bold text-green-600">432ms</div>
                    <div className="text-xs text-green-600">✓ Within SLA</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 mb-1">p99 Latency</div>
                    <div className="text-2xl font-bold text-yellow-600">891ms</div>
                    <div className="text-xs text-yellow-600">⚠ Near threshold</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 mb-1">Success Rate</div>
                    <div className="text-2xl font-bold text-green-600">99.95%</div>
                    <div className="text-xs text-green-600">✓ Exceeds SLA</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Monitoring & Alerting */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              <h2 className="text-2xl font-bold mb-6">Monitoring & Alerting</h2>

              <div className="space-y-4">
                <div className="border-l-4 border-red-500 bg-red-50 rounded-r-lg p-4">
                  <h3 className="font-bold text-red-800 mb-2">Critical Alerts (PagerDuty)</h3>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>• API error rate > 1% for 5 minutes</li>
                    <li>• Database connection failures</li>
                    <li>• Service completely down</li>
                    <li>• Disk usage > 90%</li>
                  </ul>
                </div>

                <div className="border-l-4 border-yellow-500 bg-yellow-50 rounded-r-lg p-4">
                  <h3 className="font-bold text-yellow-800 mb-2">Warning Alerts (Email)</h3>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>• p95 latency &gt; 800ms for 10 minutes</li>
                    <li>• Error rate &gt; 0.5% for 5 minutes</li>
                    <li>• CPU usage &gt; 80% for 15 minutes</li>
                    <li>• Memory usage &gt; 85%</li>
                  </ul>
                </div>

                <div className="border-l-4 border-blue-500 bg-blue-50 rounded-r-lg p-4">
                  <h3 className="font-bold text-blue-800 mb-2">Info Alerts (Slack)</h3>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>• Deployment completed</li>
                    <li>• Backup completed successfully</li>
                    <li>• Auto-scale event triggered</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer CTA */}
      <section className="bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Production-Ready HA/DR Architecture</h2>
          <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
            Demonstrating enterprise-grade high availability and disaster recovery planning for
            mission-critical AI/ML platform infrastructure.
          </p>
          <div className="flex justify-center gap-4">
            <a
              href="/tech-sops"
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors"
            >
              View Tech SOPs
            </a>
            <a
              href="/kubernetes"
              className="px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-medium transition-colors"
            >
              Kubernetes Expertise
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
