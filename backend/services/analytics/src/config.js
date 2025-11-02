// Analytics Service Configuration
require('dotenv').config();

module.exports = {
  // Service info
  serviceName: process.env.SERVICE_NAME || 'analytics',
  serviceVersion: process.env.SERVICE_VERSION || '1.0.0',
  environment: process.env.ENVIRONMENT || 'development',

  // Server config
  port: parseInt(process.env.PORT || '8002', 10),

  // Redis config
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379', 10),
    password: process.env.REDIS_PASSWORD || undefined,
    db: parseInt(process.env.REDIS_DB || '0', 10),
  },

  // CORS
  corsOrigin: process.env.CORS_ORIGIN || '*',

  // Django backend
  djangoApiUrl: process.env.DJANGO_API_URL || 'http://localhost:8000',

  // Analytics settings
  eventRetentionDays: parseInt(process.env.EVENT_RETENTION_DAYS || '30', 10),
  metricsWindowMinutes: parseInt(process.env.METRICS_WINDOW_MINUTES || '60', 10),
};
