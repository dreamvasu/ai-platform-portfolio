import { motion } from 'framer-motion';

export default function Hero() {
  return (
    <section className="bg-gradient-to-b from-gray-900 to-gray-800 text-white min-h-screen flex items-center">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <motion.h1
            className="text-5xl md:text-7xl font-bold mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            From 65% Match to 90% Match
            <br />
            <span className="text-blue-500">in 12 Hours</span>
          </motion.h1>

          <motion.p
            className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            How I transformed into an AI/ML Platform Engineer through an intense learning sprint
          </motion.p>

          <motion.div
            className="flex justify-center gap-4 flex-wrap"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
          >
            <a
              href="/journey"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition"
            >
              View Journey
            </a>
            <a
              href="#demos"
              className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-8 rounded-lg transition"
            >
              Live Demos
            </a>
            <a
              href="https://github.com/yourusername/ai-platform-portfolio"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-8 rounded-lg transition"
            >
              GitHub
            </a>
          </motion.div>

          {/* Stats Section */}
          <motion.div
            className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-500">8</div>
              <div className="text-gray-400 mt-2">Technologies Mastered</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-500">12</div>
              <div className="text-gray-400 mt-2">Hours Invested</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-500">50+</div>
              <div className="text-gray-400 mt-2">GitHub Commits</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-500">3</div>
              <div className="text-gray-400 mt-2">Live Deployments</div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
