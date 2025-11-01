export default function GCP() {
  return (
    <div className="min-h-screen bg-gray-50 py-20">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold mb-4">Google Cloud Platform</h1>
          <p className="text-xl text-gray-600">
            Hands-on GCP AI Platform & Cloud Run Experience
          </p>
        </div>

        {/* Why GCP */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-8 rounded-lg shadow-lg mb-8">
          <h2 className="text-3xl font-bold mb-4">Why GCP for This Project?</h2>
          <p className="mb-4">
            The Wipro AI/ML Platform Engineer role specifically states:{" "}
            <em>"Strong understanding of private and public cloud technologies... GCP experience preferred."</em>
          </p>
          <p className="mb-4">
            This portfolio demonstrates hands-on GCP expertise by implementing production services
            using Google Cloud's AI and serverless platforms.
          </p>
          <div className="grid md:grid-cols-2 gap-4 mt-6">
            <div className="bg-white/10 p-4 rounded">
              <h3 className="font-bold mb-2">✅ Services Used</h3>
              <ul className="space-y-1 text-sm">
                <li>• Vertex AI (Embeddings + Gemini)</li>
                <li>• Cloud Run (Serverless containers)</li>
                <li>• Cloud Build (CI/CD)</li>
                <li>• IAM (Service accounts)</li>
              </ul>
            </div>
            <div className="bg-white/10 p-4 rounded">
              <h3 className="font-bold mb-2">✅ Skills Demonstrated</h3>
              <ul className="space-y-1 text-sm">
                <li>• GCP Console navigation</li>
                <li>• gcloud CLI proficiency</li>
                <li>• Service account management</li>
                <li>• API authentication</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Vertex AI Section */}
        <div className="bg-white p-8 rounded-lg shadow-lg mb-8">
          <h2 className="text-3xl font-bold mb-4">Vertex AI Integration</h2>
          <p className="text-gray-700 mb-4">
            Vertex AI is Google's unified ML platform. For this portfolio, I used two key services:
          </p>

          <div className="space-y-6">
            {/* Text Embeddings */}
            <div className="border-l-4 border-green-500 pl-4">
              <h3 className="text-xl font-semibold mb-2">1. Text Embeddings (textembedding-gecko@003)</h3>
              <p className="text-gray-700 mb-3">
                Converts text into 768-dimensional vectors for semantic search in the RAG system.
              </p>
              <div className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
                <pre>{`from vertexai.language_models import TextEmbeddingModel
import vertexai

# Initialize Vertex AI
vertexai.init(project='your-project-id', location='us-central1')

# Load embedding model
model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")

# Generate embeddings
texts = ["Document chunk 1", "Document chunk 2"]
embeddings = model.get_embeddings(texts)

# Returns 768-dim vectors for semantic search
print(embeddings[0].values)  # [0.123, -0.456, ...]`}</pre>
              </div>
              <div className="mt-3 text-sm text-gray-600">
                <strong>Performance:</strong> ~100-200ms for batch of 250 texts |
                <strong> Cost:</strong> ~$0.00002 per 1000 characters
              </div>
            </div>

            {/* Gemini Pro */}
            <div className="border-l-4 border-purple-500 pl-4">
              <h3 className="text-xl font-semibold mb-2">2. Gemini Pro (generative AI)</h3>
              <p className="text-gray-700 mb-3">
                Google's large language model for generating intelligent, context-aware responses.
              </p>
              <div className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
                <pre>{`from vertexai.generative_models import GenerativeModel

# Initialize Gemini Pro
model = GenerativeModel("gemini-pro")

# Generate response
prompt = """Context: [Retrieved documents]

Question: How did Vasu learn Kubernetes?

Answer based on context:"""

response = model.generate_content(
    prompt,
    generation_config={
        "temperature": 0.7,
        "max_output_tokens": 500,
    }
)

print(response.text)`}</pre>
              </div>
              <div className="mt-3 text-sm text-gray-600">
                <strong>Performance:</strong> ~1-3 seconds per query |
                <strong> Cost:</strong> ~$0.00025 per 1000 characters
              </div>
            </div>
          </div>
        </div>

        {/* Cloud Run Section */}
        <div className="bg-white p-8 rounded-lg shadow-lg mb-8">
          <h2 className="text-3xl font-bold mb-4">Cloud Run Deployment</h2>
          <p className="text-gray-700 mb-4">
            Cloud Run is GCP's serverless platform for containerized applications.
            Perfect for AI/ML APIs that need auto-scaling without managing infrastructure.
          </p>

          <h3 className="text-xl font-semibold mb-3">Architecture</h3>
          <div className="bg-gray-100 p-6 rounded-lg mb-6 font-mono text-sm overflow-x-auto">
            <pre>{`
┌─────────────────────────────────────────────────────────┐
│                    HTTPS REQUEST                         │
│              https://your-service.run.app                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              CLOUD RUN SERVICE                           │
│         (Automatic HTTPS, Load Balancing)               │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌──────────────┐         ┌──────────────┐
│ Container 1  │         │ Container 2  │
│ (Django API) │         │ (Django API) │
│              │         │              │
│ • Vertex AI  │         │ • Vertex AI  │
│ • ChromaDB   │         │ • ChromaDB   │
└──────────────┘         └──────────────┘

Auto-scales 0 → 1000 instances based on traffic
Pay only for actual usage (per request)
            `}</pre>
          </div>

          <h3 className="text-xl font-semibold mb-3">Deployment Process</h3>
          <div className="space-y-4">
            <div className="bg-gray-900 text-gray-100 p-4 rounded-lg">
              <p className="text-sm text-gray-400 mb-2">1. Create Dockerfile</p>
              <pre>{`FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

CMD exec gunicorn --bind :$PORT --workers 2 core.wsgi:application`}</pre>
            </div>

            <div className="bg-gray-900 text-gray-100 p-4 rounded-lg">
              <p className="text-sm text-gray-400 mb-2">2. Deploy to Cloud Run</p>
              <pre>{`gcloud run deploy portfolio-backend \\
  --source . \\
  --region us-central1 \\
  --allow-unauthenticated \\
  --set-env-vars="GOOGLE_CLOUD_PROJECT=your-project-id" \\
  --memory=2Gi \\
  --cpu=2 \\
  --min-instances=0 \\
  --max-instances=10`}</pre>
            </div>

            <div className="bg-gray-900 text-gray-100 p-4 rounded-lg">
              <p className="text-sm text-gray-400 mb-2">3. View live service</p>
              <pre>{`gcloud run services describe portfolio-backend \\
  --region us-central1 \\
  --format='value(status.url)'`}</pre>
            </div>
          </div>

          <div className="mt-6 bg-blue-50 border-l-4 border-blue-500 p-4">
            <h4 className="font-semibold mb-2">Key Benefits for AI/ML:</h4>
            <ul className="space-y-1 text-sm text-gray-700">
              <li>• <strong>Auto-scaling:</strong> Handle traffic spikes during model inference</li>
              <li>• <strong>Cost-effective:</strong> Scale to zero when not in use</li>
              <li>• <strong>No infrastructure:</strong> Focus on code, not servers</li>
              <li>• <strong>Built-in load balancing:</strong> Distribute requests automatically</li>
              <li>• <strong>Integrated with Vertex AI:</strong> Service accounts handle authentication</li>
            </ul>
          </div>
        </div>

        {/* GCP Services Comparison */}
        <div className="bg-white p-8 rounded-lg shadow-lg mb-8">
          <h2 className="text-3xl font-bold mb-4">GCP vs Azure: What I Learned</h2>
          <p className="text-gray-700 mb-4">
            Coming from Azure experience, here's how GCP services map and what's different:
          </p>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border p-3 text-left">Category</th>
                  <th className="border p-3 text-left">Azure</th>
                  <th className="border p-3 text-left">GCP</th>
                  <th className="border p-3 text-left">Key Difference</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                <tr>
                  <td className="border p-3 font-semibold">AI Platform</td>
                  <td className="border p-3">Azure OpenAI</td>
                  <td className="border p-3">Vertex AI</td>
                  <td className="border p-3">Vertex AI more integrated with GCP services</td>
                </tr>
                <tr>
                  <td className="border p-3 font-semibold">Containers</td>
                  <td className="border p-3">Container Apps</td>
                  <td className="border p-3">Cloud Run</td>
                  <td className="border p-3">Cloud Run simpler, faster cold starts</td>
                </tr>
                <tr>
                  <td className="border p-3 font-semibold">K8s</td>
                  <td className="border p-3">AKS</td>
                  <td className="border p-3">GKE</td>
                  <td className="border p-3">GKE autopilot mode easier management</td>
                </tr>
                <tr>
                  <td className="border p-3 font-semibold">IAM</td>
                  <td className="border p-3">Azure AD</td>
                  <td className="border p-3">Cloud IAM</td>
                  <td className="border p-3">GCP uses service accounts more extensively</td>
                </tr>
                <tr>
                  <td className="border p-3 font-semibold">CLI</td>
                  <td className="border p-3">az</td>
                  <td className="border p-3">gcloud</td>
                  <td className="border p-3">gcloud more intuitive command structure</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="mt-4 text-gray-700">
            <p className="font-semibold mb-2">Learning Curve Assessment:</p>
            <p>
              Transitioning from Azure to GCP took ~2 days of hands-on experimentation.
              The core concepts (IAM, networking, containers) are identical - mainly learning
              GCP-specific terminology and console navigation.
            </p>
          </div>
        </div>

        {/* Setup & Configuration */}
        <div className="bg-white p-8 rounded-lg shadow-lg mb-8">
          <h2 className="text-3xl font-bold mb-4">Setup & Configuration</h2>

          <h3 className="text-xl font-semibold mb-3">Initial GCP Setup</h3>
          <div className="space-y-3">
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">gcloud auth login</code>
              <p className="text-sm text-gray-600 mt-1">Authenticate with GCP</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">gcloud projects create your-project-id</code>
              <p className="text-sm text-gray-600 mt-1">Create new GCP project</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">gcloud config set project your-project-id</code>
              <p className="text-sm text-gray-600 mt-1">Set active project</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">gcloud services enable aiplatform.googleapis.com</code>
              <p className="text-sm text-gray-600 mt-1">Enable Vertex AI API</p>
            </div>
          </div>

          <h3 className="text-xl font-semibold mb-3 mt-6">Service Account Setup</h3>
          <div className="space-y-3">
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">gcloud iam service-accounts create portfolio-rag</code>
              <p className="text-sm text-gray-600 mt-1">Create service account</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">gcloud projects add-iam-policy-binding ... --role="roles/aiplatform.user"</code>
              <p className="text-sm text-gray-600 mt-1">Grant Vertex AI permissions</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <code className="text-sm">gcloud iam service-accounts keys create key.json ...</code>
              <p className="text-sm text-gray-600 mt-1">Download service account key</p>
            </div>
          </div>
        </div>

        {/* Key Takeaways */}
        <div className="bg-gradient-to-r from-green-600 to-teal-600 text-white p-8 rounded-lg shadow-lg">
          <h2 className="text-3xl font-bold mb-4">Key Takeaways</h2>
          <ul className="space-y-3">
            <li className="flex items-start">
              <span className="mr-2">🌐</span>
              <span>GCP's Vertex AI is purpose-built for ML workflows - embeddings, training, deployment in one platform</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">⚡</span>
              <span>Cloud Run is ideal for ML APIs - serverless, auto-scaling, pay-per-request pricing</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">🔐</span>
              <span>Service accounts are central to GCP security - master IAM early</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">💰</span>
              <span>GCP pricing model favors bursty ML workloads - scale to zero saves money</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">🚀</span>
              <span>Multi-cloud skills are valuable - concepts transfer between Azure/GCP/AWS</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
