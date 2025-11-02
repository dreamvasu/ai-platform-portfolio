// Analytics Service - Main Server
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const config = require('./config');
const { connectRedis, isRedisConnected } = require('./redis');

// Import routes
const eventsRouter = require('./routes/events');
const metricsRouter = require('./routes/metrics');

// Create Express app
const app = express();
const server = http.createServer(app);

// Setup Socket.io
const io = new Server(server, {
  cors: {
    origin: config.corsOrigin,
    methods: ['GET', 'POST'],
  },
});

// Middleware
app.use(cors({ origin: config.corsOrigin }));
app.use(express.json());

// Request logging
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Routes
app.use('/events', eventsRouter);
app.use('/metrics', metricsRouter);

// Health check
app.get('/health', (req, res) => {
  const uptime = process.uptime();

  res.json({
    service: config.serviceName,
    version: config.serviceVersion,
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: uptime,
    environment: config.environment,
    checks: {
      redis: isRedisConnected() ? 'ok' : 'disconnected',
      websocket: io.engine.clientsCount >= 0 ? 'ok' : 'error',
    },
    clients: {
      websocket: io.engine.clientsCount,
    },
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    service: config.serviceName,
    version: config.serviceVersion,
    endpoints: {
      health: '/health',
      events: {
        pageview: 'POST /events/pageview',
        click: 'POST /events/click',
        search: 'POST /events/search',
        custom: 'POST /events/custom',
      },
      metrics: {
        popular: 'GET /metrics/popular',
        searches: 'GET /metrics/searches',
        recent: 'GET /metrics/recent',
        summary: 'GET /metrics/summary',
        realtime: 'GET /metrics/realtime',
      },
      websocket: 'WS /socket.io',
    },
  });
});

// WebSocket connection handling
io.on('connection', (socket) => {
  console.log(`Client connected: ${socket.id}`);

  socket.on('disconnect', () => {
    console.log(`Client disconnected: ${socket.id}`);
  });

  socket.on('subscribe', (data) => {
    console.log(`Client ${socket.id} subscribed to:`, data);
    if (data.channel) {
      socket.join(data.channel);
    }
  });

  socket.on('unsubscribe', (data) => {
    console.log(`Client ${socket.id} unsubscribed from:`, data);
    if (data.channel) {
      socket.leave(data.channel);
    }
  });
});

// Broadcast realtime events (example)
function broadcastEvent(eventType, data) {
  io.emit('realtime-event', { type: eventType, data, timestamp: new Date().toISOString() });
}

// Make broadcast available globally
global.broadcastEvent = broadcastEvent;

// Error handling
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
async function startServer() {
  try {
    console.log(`Starting ${config.serviceName} v${config.serviceVersion}...`);
    console.log(`Environment: ${config.environment}`);

    // Connect to Redis
    await connectRedis();

    // Start HTTP server
    server.listen(config.port, '0.0.0.0', () => {
      console.log(`✅ Server running on port ${config.port}`);
      console.log(`✅ WebSocket server ready`);
      console.log(`✅ ${config.serviceName} is ready!`);
    });
  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

// Start the server
if (require.main === module) {
  startServer();
}

module.exports = { app, server, io };
