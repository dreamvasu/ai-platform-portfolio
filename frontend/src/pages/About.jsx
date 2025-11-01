export default function About() {
  return (
    <div className="min-h-screen bg-gray-50 py-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-5xl font-bold text-center mb-12">About Me</h1>

        <div className="bg-white p-8 rounded-lg shadow mb-8">
          <h2 className="text-3xl font-bold mb-4">Vasu Kapoor</h2>
          <p className="text-xl text-gray-600 mb-4">
            Software Architect | Fast Learner | AI/ML Platform Engineer
          </p>
          <p className="text-gray-700 mb-4">
            10 years of software architecture experience, now transitioning into AI/ML platform engineering.
            This portfolio showcases my 12-hour learning sprint where I went from 65% match to 90% match
            for the Wipro AI/ML Platform Engineer role.
          </p>
          <p className="text-gray-700">
            Rather than just claiming "I can learn it," I spent 12-16 hours proving it by building a
            production-ready portfolio with RAG chatbot, Kubernetes deployments, GCP Cloud Run services,
            and Infrastructure as Code - all fully documented and deployed live.
          </p>
        </div>

        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-8 rounded-lg shadow mb-8">
          <h3 className="text-2xl font-bold mb-4">The Sprint Stats</h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div>
              <div className="text-4xl font-bold">12-16h</div>
              <div className="text-blue-100">Total Time</div>
            </div>
            <div>
              <div className="text-4xl font-bold">13</div>
              <div className="text-blue-100">Technologies</div>
            </div>
            <div>
              <div className="text-4xl font-bold">4</div>
              <div className="text-blue-100">Live Deployments</div>
            </div>
          </div>
        </div>

        <div className="bg-white p-8 rounded-lg shadow mb-8">
          <h3 className="text-2xl font-bold mb-4">What I Built</h3>
          <ul className="space-y-3">
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">✓</span>
              <span className="text-gray-700">
                <strong>Full-Stack Portfolio:</strong> React + Django REST API with real-time data
              </span>
            </li>
            <li className="flex items-start">
              <span className="text-green-600 mr-2">✓</span>
              <span className="text-gray-700">
                <strong>RAG Chatbot:</strong> Production AI system using ChromaDB + OpenAI
              </span>
            </li>
            <li className="flex items-start">
              <span className="text-purple-600 mr-2">✓</span>
              <span className="text-gray-700">
                <strong>Kubernetes Deployment:</strong> Container orchestration with auto-scaling
              </span>
            </li>
            <li className="flex items-start">
              <span className="text-orange-600 mr-2">✓</span>
              <span className="text-gray-700">
                <strong>GCP Infrastructure:</strong> Cloud Run services with Terraform IaC
              </span>
            </li>
          </ul>
        </div>

        <div className="bg-white p-8 rounded-lg shadow">
          <h3 className="text-2xl font-bold mb-4">Contact</h3>
          <p className="text-gray-600 mb-4">
            Interested in discussing AI/ML platform engineering, learning velocity, or this project?
            Let's connect!
          </p>
          <ul className="space-y-2 text-gray-700">
            <li className="flex items-center">
              <span className="mr-2">📧</span>
              <span>Email: vasu.kapoor@example.com</span>
            </li>
            <li className="flex items-center">
              <span className="mr-2">💼</span>
              <a
                href="https://linkedin.com/in/vasukapoor"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800"
              >
                LinkedIn: linkedin.com/in/vasukapoor
              </a>
            </li>
            <li className="flex items-center">
              <span className="mr-2">🐙</span>
              <a
                href="https://github.com/vasukapoor"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800"
              >
                GitHub: github.com/vasukapoor
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
