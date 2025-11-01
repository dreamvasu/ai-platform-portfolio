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
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
              {techStack.slice(0, 10).map((tech) => (
                <div key={tech.id} className="text-center p-6 bg-gray-50 rounded-lg hover:shadow-lg transition">
                  <h3 className={`text-xl font-bold mb-2 ${getColorClass(tech.color)}`}>
                    {tech.name}
                  </h3>
                  <p className="text-gray-600 text-sm">{tech.description}</p>
                  <div className="mt-3 flex justify-center">
                    {[...Array(5)].map((_, i) => (
                      <span
                        key={i}
                        className={`text-xs ${i < tech.proficiency_level ? 'text-yellow-400' : 'text-gray-300'}`}
                      >
                        ★
                      </span>
                    ))}
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

      {/* CTA Section */}
      <section className="py-20 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to see how I did it?</h2>
          <p className="text-xl text-gray-300 mb-8">
            Explore my complete learning journey and technical implementations
          </p>
          <a
            href="/journey"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition inline-block"
          >
            View Full Journey
          </a>
        </div>
      </section>
    </div>
  );
}
