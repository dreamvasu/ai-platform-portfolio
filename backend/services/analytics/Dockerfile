# Analytics Service - Production Dockerfile
# Optimized for Google Cloud Run

FROM node:20-alpine

# Set environment variables
ENV NODE_ENV=production \
    PORT=8002

# Set work directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY src/ ./src/

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S analytics -u 1001 && \
    chown -R analytics:nodejs /app

# Switch to non-root user
USER analytics

# Expose port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:8002/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start the service
CMD ["node", "src/index.js"]
