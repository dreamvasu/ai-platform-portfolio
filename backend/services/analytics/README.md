# Analytics Microservice

Node.js/Express service for real-time analytics and event tracking with Redis and WebSocket support.

## Features

- 📊 Real-time event tracking (pageviews, clicks, searches)
- 🔴 Redis-backed metrics storage
- 🌐 WebSocket support for live updates via Socket.io
- 📈 Popular pages and trending searches
- ⚡ Fast, async API endpoints
- 🐳 Docker support for Cloud Run

## Tech Stack

- **Framework:** Express.js 5.1
- **WebSocket:** Socket.io 4.8
- **Cache/Storage:** Redis 5.9
- **Runtime:** Node.js 20+

## Quick Start

### Local Development

1. **Install dependencies:**
```bash
npm install
```

2. **Setup environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start Redis (optional, service works without it):**
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

4. **Run the service:**
```bash
# Development mode (with auto-reload)
npm run dev

# Production mode
npm start
```

5. **Access the service:**
- API: http://localhost:8002
- Health: http://localhost:8002/health

## API Endpoints

### Event Tracking

#### Track Page View
```http
POST /events/pageview
Content-Type: application/json

{
  "page": "/home",
  "userId": "user123",
  "sessionId": "session456",
  "timestamp": "2025-11-03T12:00:00Z"
}
```

#### Track Click
```http
POST /events/click
Content-Type: application/json

{
  "element": "cta-button",
  "page": "/pricing",
  "userId": "user123"
}
```

#### Track Search
```http
POST /events/search
Content-Type: application/json

{
  "query": "kubernetes tutorial",
  "results": 42
}
```

#### Track Custom Event
```http
POST /events/custom
Content-Type: application/json

{
  "eventName": "video-play",
  "data": { "videoId": "abc123", "duration": 120 }
}
```

### Metrics

#### Get Popular Pages
```http
GET /metrics/popular?limit=10
```

Response:
```json
{
  "popular": [
    { "page": "/home", "views": 1234 },
    { "page": "/blog", "views": 567 }
  ]
}
```

#### Get Popular Searches
```http
GET /metrics/searches?limit=10
```

#### Get Recent Pageviews
```http
GET /metrics/recent?limit=20
```

#### Get Summary Statistics
```http
GET /metrics/summary
```

Response:
```json
{
  "totalPageviews": 5000,
  "totalClicks": 1200,
  "totalSearches": 300,
  "uniquePages": 45
}
```

#### Get Real-time Metrics
```http
GET /metrics/realtime
```

Response:
```json
{
  "active": 15,
  "eventsLastHour": 234
}
```

### Health Check
```http
GET /health
```

Response:
```json
{
  "service": "analytics",
  "version": "1.0.0",
  "status": "healthy",
  "checks": {
    "redis": "ok",
    "websocket": "ok"
  },
  "clients": {
    "websocket": 3
  }
}
```

## WebSocket Support

Connect to Socket.io for real-time updates:

```javascript
import { io } from 'socket.io-client';

const socket = io('http://localhost:8002');

// Listen for real-time events
socket.on('realtime-event', (data) => {
  console.log('Event:', data);
});

// Subscribe to specific channel
socket.emit('subscribe', { channel: 'pageviews' });
```

## Configuration

Environment variables (`.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVICE_NAME` | analytics | Service name |
| `SERVICE_VERSION` | 1.0.0 | Service version |
| `ENVIRONMENT` | development | Environment |
| `PORT` | 8002 | Server port |
| `REDIS_HOST` | localhost | Redis host |
| `REDIS_PORT` | 6379 | Redis port |
| `REDIS_PASSWORD` | - | Redis password |
| `CORS_ORIGIN` | * | CORS origin |

## Deployment

### Google Cloud Run

1. **Build and deploy:**
```bash
gcloud run deploy analytics \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production,REDIS_HOST=<memorystore-ip> \
  --port 8002
```

2. **With Redis (Memorystore):**
```bash
# Create Redis instance
gcloud redis instances create analytics-redis \
  --size=1 \
  --region=us-central1 \
  --redis-version=redis_7_0

# Get instance IP
gcloud redis instances describe analytics-redis --region=us-central1

# Deploy with Redis IP
gcloud run deploy analytics \
  --source . \
  --region us-central1 \
  --set-env-vars REDIS_HOST=<instance-ip>
```

### Docker

```bash
# Build image
docker build -t analytics:latest .

# Run locally
docker run -p 8002:8002 \
  -e REDIS_HOST=host.docker.internal \
  analytics:latest
```

## Project Structure

```
analytics/
├── src/
│   ├── index.js           # Main server
│   ├── config.js          # Configuration
│   ├── redis.js           # Redis client
│   └── routes/
│       ├── events.js      # Event tracking
│       └── metrics.js     # Metrics endpoints
├── package.json
├── Dockerfile
├── .env.example
└── README.md
```

## Redis Data Structures

### Keys

- `counter:pageview:<page>` - Page view counter
- `counter:click:<element>` - Click counter
- `counter:search:<query>` - Search counter
- `event:pageview:<id>` - Page view event (30 day TTL)
- `event:click:<id>` - Click event (30 day TTL)
- `recent:pageviews` - List of recent pageviews (last 100)
- `popular:searches` - Sorted set of popular searches

## Testing

Test the service locally:

```bash
# Health check
curl http://localhost:8002/health

# Track pageview
curl -X POST http://localhost:8002/events/pageview \
  -H 'Content-Type: application/json' \
  -d '{"page":"/test","userId":"test123"}'

# Get metrics
curl http://localhost:8002/metrics/summary
```

## Monitoring

- Health endpoint: `/health`
- Logs: Structured JSON logging
- Metrics: Available via `/metrics/*` endpoints

## Future Enhancements

- [ ] Prometheus metrics export
- [ ] Data aggregation to Django backend
- [ ] Event batching
- [ ] Rate limiting
- [ ] User session tracking
- [ ] A/B testing support
- [ ] Custom dashboard UI

## License

Part of AI/ML Platform Engineer Portfolio

---

**Built with Express & Socket.io** | **Deployed on Cloud Run** | **Vasu Kapoor 2025**
