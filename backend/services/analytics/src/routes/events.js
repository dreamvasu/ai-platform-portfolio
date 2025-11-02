// Event Tracking Endpoints
const express = require('express');
const router = express.Router();
const { getRedisClient, isRedisConnected } = require('../redis');

// Track page view
router.post('/pageview', async (req, res) => {
  try {
    const { page, userId, sessionId, timestamp } = req.body;

    if (!page) {
      return res.status(400).json({ error: 'Page is required' });
    }

    const event = {
      type: 'pageview',
      page,
      userId: userId || 'anonymous',
      sessionId: sessionId || null,
      timestamp: timestamp || new Date().toISOString(),
    };

    // Store in Redis if connected
    if (isRedisConnected()) {
      const redis = getRedisClient();
      const key = `event:pageview:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`;

      // Store event
      await redis.setEx(key, 60 * 60 * 24 * 30, JSON.stringify(event)); // 30 days TTL

      // Increment page counter
      await redis.incr(`counter:pageview:${page}`);

      // Add to recent pageviews list
      await redis.lPush('recent:pageviews', JSON.stringify(event));
      await redis.lTrim('recent:pageviews', 0, 99); // Keep last 100
    }

    res.json({ success: true, event });
  } catch (error) {
    console.error('Error tracking pageview:', error);
    res.status(500).json({ error: 'Failed to track pageview' });
  }
});

// Track click event
router.post('/click', async (req, res) => {
  try {
    const { element, page, userId, sessionId, timestamp } = req.body;

    if (!element) {
      return res.status(400).json({ error: 'Element is required' });
    }

    const event = {
      type: 'click',
      element,
      page: page || 'unknown',
      userId: userId || 'anonymous',
      sessionId: sessionId || null,
      timestamp: timestamp || new Date().toISOString(),
    };

    // Store in Redis if connected
    if (isRedisConnected()) {
      const redis = getRedisClient();
      const key = `event:click:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`;

      await redis.setEx(key, 60 * 60 * 24 * 30, JSON.stringify(event));
      await redis.incr(`counter:click:${element}`);
    }

    res.json({ success: true, event });
  } catch (error) {
    console.error('Error tracking click:', error);
    res.status(500).json({ error: 'Failed to track click' });
  }
});

// Track search query
router.post('/search', async (req, res) => {
  try {
    const { query, results, userId, sessionId, timestamp } = req.body;

    if (!query) {
      return res.status(400).json({ error: 'Query is required' });
    }

    const event = {
      type: 'search',
      query,
      results: results || 0,
      userId: userId || 'anonymous',
      sessionId: sessionId || null,
      timestamp: timestamp || new Date().toISOString(),
    };

    // Store in Redis if connected
    if (isRedisConnected()) {
      const redis = getRedisClient();
      const key = `event:search:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`;

      await redis.setEx(key, 60 * 60 * 24 * 30, JSON.stringify(event));
      await redis.incr(`counter:search:${query}`);

      // Add to popular searches
      await redis.zIncrBy('popular:searches', 1, query);
    }

    res.json({ success: true, event });
  } catch (error) {
    console.error('Error tracking search:', error);
    res.status(500).json({ error: 'Failed to track search' });
  }
});

// Track custom event
router.post('/custom', async (req, res) => {
  try {
    const { eventName, data, userId, sessionId, timestamp } = req.body;

    if (!eventName) {
      return res.status(400).json({ error: 'Event name is required' });
    }

    const event = {
      type: 'custom',
      eventName,
      data: data || {},
      userId: userId || 'anonymous',
      sessionId: sessionId || null,
      timestamp: timestamp || new Date().toISOString(),
    };

    // Store in Redis if connected
    if (isRedisConnected()) {
      const redis = getRedisClient();
      const key = `event:custom:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`;

      await redis.setEx(key, 60 * 60 * 24 * 30, JSON.stringify(event));
      await redis.incr(`counter:custom:${eventName}`);
    }

    res.json({ success: true, event });
  } catch (error) {
    console.error('Error tracking custom event:', error);
    res.status(500).json({ error: 'Failed to track custom event' });
  }
});

module.exports = router;
