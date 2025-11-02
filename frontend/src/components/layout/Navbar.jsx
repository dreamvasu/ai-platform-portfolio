import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-gray-900 text-white fixed w-full z-50 top-0">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold">
              Vasu Kapoor
            </Link>
          </div>

          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <Link to="/" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
                Home
              </Link>
              <Link to="/journey" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
                Journey
              </Link>
              <Link to="/papers" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
                Papers
              </Link>
              <Link to="/kubernetes" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
                Kubernetes
              </Link>
              <Link to="/gcp" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
                GCP
              </Link>
              <Link to="/rag" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
                RAG
              </Link>
              <Link to="/case-studies" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
                Case Studies
              </Link>
              <Link to="/about" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
                About
              </Link>
              <a
                href="https://github.com/yourusername/ai-platform-portfolio"
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700"
              >
                GitHub
              </a>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
