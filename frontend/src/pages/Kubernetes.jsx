export default function Kubernetes() {
  return (
    <div className="min-h-screen bg-gray-50 py-20">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold mb-4">Kubernetes Deep Dive</h1>
          <p className="text-xl text-gray-600">
            Container orchestration for the AI/ML Portfolio
          </p>
        </div>

        {/* Overview */}
        <div className="bg-white p-8 rounded-lg shadow-lg mb-8">
          <h2 className="text-3xl font-bold mb-4">Overview</h2>
          <p className="text-gray-700 mb-4">
            Kubernetes (K8s) is a container orchestration platform that automates deployment,
            scaling, and management of containerized applications. For AI/ML platforms, K8s provides:
          </p>
          <ul className="space-y-2 text-gray-700">
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">✓</span>
              <span><strong>Auto-scaling:</strong> Scale AI workloads based on demand</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">✓</span>
              <span><strong>High Availability:</strong> Self-healing and fault tolerance</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">✓</span>
              <span><strong>Resource Management:</strong> Efficient GPU/CPU allocation</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">✓</span>
              <span><strong>Rolling Updates:</strong> Zero-downtime deployments</span>
            </li>
          </ul>
        </div>

        {/* What I Learned */}
        <div className="bg-white p-8 rounded-lg shadow-lg mb-8">
          <h2 className="text-3xl font-bold mb-4">What I Learned</h2>
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-semibold mb-2 text-blue-600">Core Concepts</h3>
              <ul className="space-y-2 text-gray-700 ml-4">
                <li><strong>Pods:</strong> Smallest deployable units, can contain multiple containers</li>
                <li><strong>Deployments:</strong> Declarative updates for Pods and ReplicaSets</li>
                <li><strong>Services:</strong> Stable network endpoints for accessing Pods</li>
                <li><strong>ConfigMaps & Secrets:</strong> Configuration and sensitive data management</li>
                <li><strong>Ingress:</strong> HTTP/HTTPS routing to services</li>
                <li><strong>HPA:</strong> Horizontal Pod Autoscaler for dynamic scaling</li>
              </ul>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-2 text-green-600">Hands-On Experience</h3>
              <ul className="space-y-2 text-gray-700 ml-4">
                <li>Set up local K8s cluster with Minikube</li>
                <li>Wrote YAML manifests for Django backend deployment</li>
                <li>Configured LoadBalancer service for external access</li>
                <li>Implemented Horizontal Pod Autoscaling based on CPU</li>
                <li>Created health check probes (liveness & readiness)</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Implementation */}
        <div className="bg-white p-8 rounded-lg shadow-lg mb-8">
          <h2 className="text-3xl font-bold mb-4">Implementation</h2>

          <h3 className="text-xl font-semibold mb-3">Architecture</h3>
          <div className="bg-gray-100 p-6 rounded-lg mb-6 font-mono text-sm overflow-x-auto">
            <pre>{`
┌─────────────────────────────────────────────────────┐
│                  LOAD BALANCER                       │
│              (External IP: xxx.xxx.xxx.xxx)         │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                K8S SERVICE                           │
│            (ClusterIP/LoadBalancer)                  │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌──────────────┐         ┌──────────────┐
│   POD 1      │         │   POD 2      │
│              │         │              │
│ ┌──────────┐ │         │ ┌──────────┐ │
│ │ Django   │ │         │ │ Django   │ │
│ │ Backend  │ │         │ │ Backend  │ │
│ └──────────┘ │         │ └──────────┘ │
└──────────────┘         └──────────────┘
        │                         │
        └─────────┬───────────────┘
                  ▼
         ┌──────────────┐
         │   DATABASE   │
         │  (External)  │
         └──────────────┘
            `}</pre>
          </div>

          <h3 className="text-xl font-semibold mb-3">Key Manifests</h3>

          <div className="mb-6">
            <h4 className="font-semibold text-lg mb-2">Deployment YAML</h4>
            <div className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
              <pre>{`apiVersion: apps/v1
kind: Deployment
metadata:
  name: portfolio-backend
  labels:
    app: portfolio
    tier: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: portfolio
      tier: backend
  template:
    metadata:
      labels:
        app: portfolio
        tier: backend
    spec:
      containers:
      - name: django
        image: gcr.io/PROJECT_ID/portfolio-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DJANGO_SETTINGS_MODULE
          value: "core.settings"
        - name: GOOGLE_CLOUD_PROJECT
          valueFrom:
            secretKeyRef:
              name: gcp-credentials
              key: project_id
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5`}</pre>
            </div>
          </div>

          <div className="mb-6">
            <h4 className="font-semibold text-lg mb-2">Service YAML</h4>
            <div className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
              <pre>{`apiVersion: v1
kind: Service
metadata:
  name: portfolio-backend-service
spec:
  type: LoadBalancer
  selector:
    app: portfolio
    tier: backend
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  sessionAffinity: ClientIP`}</pre>
            </div>
          </div>

          <div className="mb-6">
            <h4 className="font-semibold text-lg mb-2">Horizontal Pod Autoscaler</h4>
            <div className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
              <pre>{`apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: portfolio-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: portfolio-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70`}</pre>
            </div>
          </div>
        </div>

        {/* Challenges & Solutions */}
        <div className="bg-white p-8 rounded-lg shadow-lg mb-8">
          <h2 className="text-3xl font-bold mb-4">Challenges & Solutions</h2>
          <div className="space-y-4">
            <div className="border-l-4 border-orange-500 pl-4">
              <h3 className="font-semibold text-lg mb-2">Challenge: Pod Networking</h3>
              <p className="text-gray-700 mb-2">
                Initial confusion about how Pods communicate with each other and external services.
              </p>
              <p className="text-gray-700">
                <strong>Solution:</strong> Learned about Services (ClusterIP, NodePort, LoadBalancer)
                and how they provide stable networking abstractions.
              </p>
            </div>

            <div className="border-l-4 border-blue-500 pl-4">
              <h3 className="font-semibold text-lg mb-2">Challenge: Resource Limits</h3>
              <p className="text-gray-700 mb-2">
                Pods getting OOMKilled due to memory limits.
              </p>
              <p className="text-gray-700">
                <strong>Solution:</strong> Set appropriate resource requests and limits based on
                actual application usage. Used metrics-server to monitor resource consumption.
              </p>
            </div>

            <div className="border-l-4 border-green-500 pl-4">
              <h3 className="font-semibold text-lg mb-2">Challenge: ConfigMap vs Secrets</h3>
              <p className="text-gray-700 mb-2">
                Understanding when to use ConfigMaps vs Secrets.
              </p>
              <p className="text-gray-700">
                <strong>Solution:</strong> ConfigMaps for non-sensitive config (feature flags, URLs),
                Secrets for sensitive data (API keys, passwords). Both base64 encoded.
              </p>
            </div>
          </div>
        </div>

        {/* Commands Cheat Sheet */}
        <div className="bg-white p-8 rounded-lg shadow-lg mb-8">
          <h2 className="text-3xl font-bold mb-4">Common Commands</h2>
          <div className="space-y-3">
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">kubectl apply -f deployment.yaml</code>
              <p className="text-sm text-gray-600 mt-1">Apply deployment manifest</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">kubectl get pods -w</code>
              <p className="text-sm text-gray-600 mt-1">Watch pod status in real-time</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">kubectl logs POD_NAME -f</code>
              <p className="text-sm text-gray-600 mt-1">Stream pod logs</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">kubectl describe pod POD_NAME</code>
              <p className="text-sm text-gray-600 mt-1">Get detailed pod information</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">kubectl scale deployment portfolio-backend --replicas=5</code>
              <p className="text-sm text-gray-600 mt-1">Manually scale deployment</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">kubectl port-forward pod/POD_NAME 8000:8000</code>
              <p className="text-sm text-gray-600 mt-1">Access pod locally for debugging</p>
            </div>
          </div>
        </div>

        {/* Key Takeaways */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-8 rounded-lg shadow-lg">
          <h2 className="text-3xl font-bold mb-4">Key Takeaways</h2>
          <ul className="space-y-3">
            <li className="flex items-start">
              <span className="mr-2">🎯</span>
              <span>Kubernetes is essential for production AI/ML platforms - enables scalability and reliability</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">📚</span>
              <span>Learning curve is steep but concepts are transferable across cloud providers</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">🚀</span>
              <span>YAML manifests are infrastructure as code - version control everything</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">💡</span>
              <span>Start simple (single deployment) then add complexity (HPA, ingress, monitoring)</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">🔧</span>
              <span>kubectl is your best friend - master the CLI before relying on dashboards</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
