import { useState, useEffect } from 'react';
import { getPapers } from '../services/api';
import { ExternalLink, Calendar, User, Tag } from 'lucide-react';

export default function Papers() {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('published_date');

  useEffect(() => {
    const fetchPapers = async () => {
      try {
        const data = await getPapers({ ordering: `-${sortBy}` });
        setPapers(data.results || []);
      } catch (error) {
        console.error('Error fetching papers:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPapers();
  }, [sortBy]);

  const getCategoryColor = (category) => {
    const colors = {
      llm: 'bg-blue-100 text-blue-700',
      nlp: 'bg-green-100 text-green-700',
      multimodal: 'bg-purple-100 text-purple-700',
      mlops: 'bg-orange-100 text-orange-700',
    };
    return colors[category] || 'bg-gray-100 text-gray-700';
  };

  const filteredPapers = filter === 'all'
    ? papers
    : papers.filter(p => p.category === filter);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-gray-900 to-gray-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-5xl font-bold mb-4">AI Industry Updates</h1>
          <p className="text-xl text-gray-300 max-w-3xl">
            Latest model releases, research breakthroughs, and AI company announcements from OpenAI, Google AI, Microsoft, HuggingFace, and more. Automatically scraped and curated to keep you ahead of industry trends.
          </p>
          <div className="mt-8 flex items-center gap-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-3xl font-bold text-blue-400">{papers.length}</div>
              <div className="text-sm text-gray-300">Blog Posts</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-3xl font-bold text-green-400">Live</div>
              <div className="text-sm text-gray-300">Auto-Scraped</div>
            </div>
          </div>
        </div>
      </section>

      {/* Filters and Sort */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-wrap gap-4 items-center justify-between">
            <div className="flex gap-2">
              {['all', 'llm', 'nlp', 'multimodal', 'mlops'].map((cat) => (
                <button
                  key={cat}
                  onClick={() => setFilter(cat)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all uppercase ${
                    filter === cat
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {cat === 'all' ? 'All' : cat}
                </button>
              ))}
            </div>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="published_date">Latest First</option>
              <option value="relevance_score">Most Relevant</option>
              <option value="citation_count">Most Cited</option>
            </select>
          </div>
        </div>
      </div>

      {/* Papers List */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {loading ? (
          <div className="text-center text-gray-500 py-20">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p>Loading AI updates...</p>
          </div>
        ) : filteredPapers.length === 0 ? (
          <div className="text-center text-gray-500 py-20">
            <p className="text-xl">No updates found for this filter.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {filteredPapers.map((paper) => (
              <article
                key={paper.id}
                className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 hover:shadow-xl transition-all duration-300 group"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h2 className="text-2xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">
                      {paper.title}
                    </h2>
                    <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-4">
                      <span className="flex items-center gap-1">
                        <User className="w-4 h-4" />
                        {paper.authors}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {new Date(paper.published_date).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </span>
                      {paper.citation_count > 0 && (
                        <span className="flex items-center gap-1 font-medium text-blue-600">
                          📊 {paper.citation_count} citations
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2 ml-4">
                    {paper.relevance_score >= 0.7 && (
                      <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-medium">
                        Highly Relevant
                      </span>
                    )}
                    <span className={`px-3 py-1 rounded-full text-xs font-medium capitalize ${getCategoryColor(paper.category)}`}>
                      {paper.category}
                    </span>
                  </div>
                </div>

                {paper.abstract && (
                  <p className="text-gray-700 leading-relaxed mb-4">
                    {paper.abstract.length > 400
                      ? `${paper.abstract.slice(0, 400)}...`
                      : paper.abstract}
                  </p>
                )}

                {paper.tags && Array.isArray(paper.tags) && paper.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {paper.tags.map((tag, idx) => (
                      <span
                        key={idx}
                        className="flex items-center gap-1 px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs"
                      >
                        <Tag className="w-3 h-3" />
                        {tag}
                      </span>
                    ))}
                  </div>
                )}

                <div className="flex gap-4 pt-4 border-t border-gray-100">
                  <a
                    href={paper.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-blue-600 hover:text-blue-800 font-medium transition-colors"
                  >
                    <ExternalLink className="w-4 h-4" />
                    Read Full Article
                  </a>
                  <span className="text-sm text-gray-500">
                    {paper.source_display}
                  </span>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>

      {/* Stats Section */}
      {!loading && papers.length > 0 && (
        <section className="bg-gray-900 text-white py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold mb-8 text-center">AI Updates Metrics</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 text-center">
                <div className="text-4xl font-bold text-blue-400 mb-2">{papers.length}</div>
                <div className="text-sm text-gray-300">Total Updates</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 text-center">
                <div className="text-4xl font-bold text-green-400 mb-2">
                  {papers.filter(p => p.relevance_score >= 0.7).length}
                </div>
                <div className="text-sm text-gray-300">Highly Relevant</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 text-center">
                <div className="text-4xl font-bold text-purple-400 mb-2">
                  {new Set(papers.map(p => p.category)).size}
                </div>
                <div className="text-sm text-gray-300">Categories</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 text-center">
                <div className="text-4xl font-bold text-orange-400 mb-2">
                  {new Set(papers.map(p => p.source_display)).size}
                </div>
                <div className="text-sm text-gray-300">AI Companies</div>
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
