import { useState, useEffect } from 'react';
import { getJourneyEntries } from '../services/api';

export default function Journey() {
  const [journeyEntries, setJourneyEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJourney = async () => {
      try {
        const data = await getJourneyEntries();
        setJourneyEntries(data.results || []);
      } catch (error) {
        console.error('Error fetching journey:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchJourney();
  }, []);

  const getColorClass = (color) => {
    const colors = {
      blue: 'bg-blue-100 text-blue-800',
      green: 'bg-green-100 text-green-800',
      purple: 'bg-purple-100 text-purple-800',
      orange: 'bg-orange-100 text-orange-800',
      red: 'bg-red-100 text-red-800',
      yellow: 'bg-yellow-100 text-yellow-800',
      cyan: 'bg-cyan-100 text-cyan-800',
      pink: 'bg-pink-100 text-pink-800',
      emerald: 'bg-emerald-100 text-emerald-800',
    };
    return colors[color] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-20">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-5xl font-bold text-center mb-6">My Journey</h1>
        <p className="text-xl text-gray-600 text-center mb-16">
          A 12-hour sprint to master AI/ML Platform Engineering
        </p>

        {loading ? (
          <div className="text-center text-gray-500">Loading journey...</div>
        ) : (
          <div className="relative">
            {/* Timeline line */}
            <div className="absolute left-8 top-0 bottom-0 w-1 bg-blue-200"></div>

            {/* Journey entries */}
            <div className="space-y-12">
              {journeyEntries.map((entry, index) => (
                <div key={entry.id} className="relative pl-20">
                  {/* Hour badge */}
                  <div className="absolute left-0 top-0 w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-lg shadow-lg">
                    H{entry.hour}
                  </div>

                  {/* Entry card */}
                  <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
                    <h3 className="text-2xl font-bold mb-4 text-gray-900">
                      {entry.title}
                    </h3>

                    <div className="space-y-4">
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">What I Learned:</h4>
                        <p className="text-gray-600">{entry.description}</p>
                      </div>

                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Challenges:</h4>
                        <p className="text-gray-600">{entry.challenges}</p>
                      </div>

                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Outcomes:</h4>
                        <p className="text-gray-600">{entry.outcomes}</p>
                      </div>

                      {/* Tech stack tags */}
                      {entry.tech_stack && entry.tech_stack.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-gray-700 mb-2">Technologies:</h4>
                          <div className="flex flex-wrap gap-2">
                            {entry.tech_stack.map((tech) => (
                              <span
                                key={tech.id}
                                className={`px-3 py-1 rounded-full text-xs font-medium ${getColorClass(tech.color)}`}
                              >
                                {tech.name}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Summary stats */}
        {!loading && journeyEntries.length > 0 && (
          <div className="mt-16 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-8 rounded-lg">
            <h3 className="text-2xl font-bold mb-4 text-center">Sprint Summary</h3>
            <div className="grid grid-cols-3 gap-8 text-center">
              <div>
                <div className="text-4xl font-bold">{journeyEntries.length}</div>
                <div className="text-blue-100">Hours Logged</div>
              </div>
              <div>
                <div className="text-4xl font-bold">
                  {new Set(journeyEntries.flatMap(e => e.tech_stack.map(t => t.id))).size}
                </div>
                <div className="text-blue-100">Technologies</div>
              </div>
              <div>
                <div className="text-4xl font-bold">100%</div>
                <div className="text-blue-100">Committed</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
