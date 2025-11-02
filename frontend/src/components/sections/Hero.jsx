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
            AI/ML Platform Engineer
            <br />
            <span className="text-blue-500">Production-Ready Solutions</span>
          </motion.h1>

          <motion.p
            className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            Building scalable cloud platforms with Kubernetes, multi-tenant architectures, and production-grade deployments
          </motion.p>

          <motion.div
            className="flex justify-center gap-4 flex-wrap"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
          >
            <a
              href="/case-studies"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition"
            >
              View Case Studies
            </a>
            <a
              href="#projects"
              className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-8 rounded-lg transition"
            >
              Production Projects
            </a>
            <a
              href="https://github.com/dreamvasu"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-8 rounded-lg transition"
            >
              GitHub Portfolio
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
              <div className="text-4xl font-bold text-blue-500">10K+</div>
              <div className="text-gray-400 mt-2">Requests Processed Daily</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-500">99.9%</div>
              <div className="text-gray-400 mt-2">Production Uptime</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-500">20+</div>
              <div className="text-gray-400 mt-2">Enterprise Tenants</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-500">3</div>
              <div className="text-gray-400 mt-2">Production Platforms</div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
