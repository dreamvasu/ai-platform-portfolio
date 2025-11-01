export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-bold mb-4">Vasu Kapoor</h3>
            <p className="text-gray-400">
              AI/ML Platform Engineer | Fast Learner | Code Shipper
            </p>
          </div>

          <div>
            <h3 className="text-lg font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-gray-400">
              <li><a href="/journey" className="hover:text-white">Journey</a></li>
              <li><a href="/about" className="hover:text-white">About</a></li>
              <li><a href="https://github.com/yourusername" target="_blank" rel="noopener noreferrer" className="hover:text-white">GitHub</a></li>
              <li><a href="https://linkedin.com/in/yourprofile" target="_blank" rel="noopener noreferrer" className="hover:text-white">LinkedIn</a></li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-bold mb-4">Technologies</h3>
            <div className="flex flex-wrap gap-2">
              <span className="bg-blue-600 px-2 py-1 rounded text-sm">React</span>
              <span className="bg-green-600 px-2 py-1 rounded text-sm">Django</span>
              <span className="bg-purple-600 px-2 py-1 rounded text-sm">Kubernetes</span>
              <span className="bg-orange-600 px-2 py-1 rounded text-sm">GCP</span>
              <span className="bg-red-600 px-2 py-1 rounded text-sm">Terraform</span>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-800 text-center text-gray-400">
          <p>&copy; {new Date().getFullYear()} Vasu Kapoor. Built in 12 hours.</p>
        </div>
      </div>
    </footer>
  );
}
