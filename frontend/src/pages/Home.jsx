import { useState, useEffect } from 'react';
import Hero from '../components/sections/Hero';
import { getTechStack, getFeaturedProjects } from '../services/api';

export default function Home() {
  const [techStack, setTechStack] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [techData, projectsData] = await Promise.all([
          getTechStack(),
          getFeaturedProjects()
        ]);
        setTechStack(techData.results || []);
        setProjects(projectsData || []);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getColorClass = (color) => {
    const colors = {
      blue: 'text-blue-600',
      green: 'text-green-600',
      purple: 'text-purple-600',
      orange: 'text-orange-600',
      red: 'text-red-600',
      yellow: 'text-yellow-600',
      cyan: 'text-cyan-600',
      pink: 'text-pink-600',
      emerald: 'text-emerald-600',
    };
    return colors[color] || 'text-gray-600';
  };

  return (
    <div>
      <Hero />

      {/* Tech Stack Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center mb-12">Tech Stack</h2>

          {loading ? (
            <div className="text-center text-gray-500">Loading tech stack...</div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
              {techStack.slice(0, 12).map((tech) => (
                <div key={tech.id} className="group p-6 bg-white rounded-xl border border-gray-200 hover:border-blue-500 hover:shadow-xl transition-all duration-300">
                  <h3 className={`text-2xl font-bold mb-3 ${getColorClass(tech.color)}`}>
                    {tech.name}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4 leading-relaxed">{tech.description}</p>
                  <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
                    <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                      {tech.proficiency_level === 5 ? 'Expert' :
                       tech.proficiency_level === 4 ? 'Advanced' :
                       tech.proficiency_level === 3 ? 'Proficient' :
                       tech.proficiency_level === 2 ? 'Intermediate' : 'Familiar'}
                    </span>
                    <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className={`h-full bg-gradient-to-r ${
                          tech.proficiency_level === 5 ? 'from-green-500 to-emerald-600' :
                          tech.proficiency_level === 4 ? 'from-blue-500 to-blue-600' :
                          tech.proficiency_level === 3 ? 'from-yellow-500 to-orange-500' :
                          'from-gray-400 to-gray-500'
                        }`}
                        style={{ width: `${(tech.proficiency_level / 5) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Featured Projects Section */}
      {!loading && projects.length > 0 && (
        <section className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-4xl font-bold text-center mb-12">Featured Projects</h2>
            <div className="grid md:grid-cols-2 gap-8">
              {projects.map((project) => (
                <div key={project.id} className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
                  <h3 className="text-2xl font-bold mb-4">{project.title}</h3>
                  <p className="text-gray-600 mb-4">{project.description}</p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {project.tech_stack.map((tech) => (
                      <span
                        key={tech.id}
                        className={`px-3 py-1 rounded text-sm font-medium bg-${tech.color}-100 ${getColorClass(tech.color)}`}
                      >
                        {tech.name}
                      </span>
                    ))}
                  </div>
                  <div className="flex gap-4">
                    {project.github_url && (
                      <a
                        href={project.github_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 font-medium"
                      >
                        GitHub →
                      </a>
                    )}
                    {project.live_url && (
                      <a
                        href={project.live_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-green-600 hover:text-green-800 font-medium"
                      >
                        Live Demo →
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Live Microservices Section */}
      <section className="py-20 bg-gradient-to-b from-white to-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Live Production Microservices</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              This portfolio itself runs on a production microservices architecture with real-time data processing
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-xl shadow-lg p-8 border-t-4 border-blue-500">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">Paper Scraper</h3>
                <span className="flex items-center gap-2 text-green-600 text-sm font-medium">
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  Live
                </span>
              </div>
              <p className="text-gray-600 mb-4">
                FastAPI service scraping arXiv papers with ML/AI categorization and relevance scoring
              </p>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Tech Stack:</span>
                  <span className="font-medium">FastAPI, Pydantic</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Deployment:</span>
                  <span className="font-medium">Cloud Run</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Papers Scraped:</span>
                  <span className="font-medium text-blue-600">{papers.length}+</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-8 border-t-4 border-green-500">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">Django Backend</h3>
                <span className="flex items-center gap-2 text-green-600 text-sm font-medium">
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  Live
                </span>
              </div>
              <p className="text-gray-600 mb-4">
                RESTful API serving portfolio data with webhook integration and multi-tenant architecture patterns
              </p>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Tech Stack:</span>
                  <span className="font-medium">Django, PostgreSQL</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Deployment:</span>
                  <span className="font-medium">Cloud Run + Cloud SQL</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">API Endpoints:</span>
                  <span className="font-medium text-green-600">12+</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-8 border-t-4 border-purple-500">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">Document Processor</h3>
                <span className="flex items-center gap-2 text-green-600 text-sm font-medium">
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  Live
                </span>
              </div>
              <p className="text-gray-600 mb-4">
                RAG-powered AI chatbot with vector embeddings and semantic search using ChromaDB
              </p>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Tech Stack:</span>
                  <span className="font-medium">Gemini, ChromaDB</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Deployment:</span>
                  <span className="font-medium">Cloud Run</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Embeddings:</span>
                  <span className="font-medium text-purple-600">768-dim</span>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-12 text-center">
            <a
              href="/papers"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition shadow-lg hover:shadow-xl"
            >
              Explore Scraped Papers →
            </a>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6">See My Work in Production</h2>
          <p className="text-xl text-gray-300 mb-8">
            Explore detailed case studies, architectural decisions, and real-world deployments
          </p>
          <a
            href="/case-studies"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition inline-block"
          >
            View Case Studies
          </a>
        </div>
      </section>
    </div>
  );
}
