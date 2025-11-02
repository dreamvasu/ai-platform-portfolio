// Redis Client Setup
const { createClient } = require('redis');
const config = require('./config');

let redisClient = null;
let isConnected = false;

// Create Redis client with proper configuration
const client = createClient({
  socket: {
    host: config.redis.host,
    port: config.redis.port,
    reconnectStrategy: (retries) => {
      // Stop retrying after 3 attempts
      if (retries > 3) {
        console.log('❌ Redis connection failed after 3 retries, giving up');
        return false; // Stop retrying
      }
      // Wait 1 second between retries
      return 1000;
    },
  },
  password: config.redis.password,
  database: config.redis.db,
});

// Error handling
client.on('error', (err) => {
  console.error('Redis Client Error:', err);
  isConnected = false;
});

client.on('connect', () => {
  console.log('Redis Client Connected');
  isConnected = true;
});

client.on('ready', () => {
  console.log('Redis Client Ready');
});

client.on('end', () => {
  console.log('Redis Client Disconnected');
  isConnected = false;
});

// Connect to Redis
async function connectRedis() {
  try {
    if (!redisClient) {
      await client.connect();
      redisClient = client;
      console.log('✅ Redis connection established');
    }
    return redisClient;
  } catch (error) {
    console.error('❌ Failed to connect to Redis:', error.message);
    // Don't throw - allow service to run without Redis for now
    return null;
  }
}

// Get Redis client
function getRedisClient() {
  return redisClient;
}

// Check if Redis is connected
function isRedisConnected() {
  return isConnected;
}

// Disconnect Redis
async function disconnectRedis() {
  if (redisClient) {
    await redisClient.quit();
    redisClient = null;
    isConnected = false;
  }
}

module.exports = {
  connectRedis,
  getRedisClient,
  isRedisConnected,
  disconnectRedis,
};
