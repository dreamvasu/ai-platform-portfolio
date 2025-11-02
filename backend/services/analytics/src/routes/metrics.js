// Metrics Endpoints
const express = require('express');
const router = express.Router();
const { getRedisClient, isRedisConnected } = require('../redis');

// Get popular pages
router.get('/popular', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit || '10', 10);

    if (!isRedisConnected()) {
      return res.json({ popular: [], message: 'Redis not connected' });
    }

    const redis = getRedisClient();

    // Get all pageview counters
    const keys = await redis.keys('counter:pageview:*');
    const popularPages = [];

    for (const key of keys) {
      const count = await redis.get(key);
      const page = key.replace('counter:pageview:', '');
      popularPages.push({ page, views: parseInt(count, 10) });
    }

    // Sort by views
    popularPages.sort((a, b) => b.views - a.views);

    res.json({ popular: popularPages.slice(0, limit) });
  } catch (error) {
    console.error('Error getting popular pages:', error);
    res.status(500).json({ error: 'Failed to get popular pages' });
  }
});

// Get popular searches
router.get('/searches', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit || '10', 10);

    if (!isRedisConnected()) {
      return res.json({ searches: [], message: 'Redis not connected' });
    }

    const redis = getRedisClient();

    // Get popular searches from sorted set
    const searches = await redis.zRangeWithScores('popular:searches', 0, limit - 1, {
      REV: true,
    });

    const formattedSearches = searches.map((item) => ({
      query: item.value,
      count: item.score,
    }));

    res.json({ searches: formattedSearches });
  } catch (error) {
    console.error('Error getting popular searches:', error);
    res.status(500).json({ error: 'Failed to get popular searches' });
  }
});

// Get recent pageviews
router.get('/recent', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit || '20', 10);

    if (!isRedisConnected()) {
      return res.json({ recent: [], message: 'Redis not connected' });
    }

    const redis = getRedisClient();

    // Get recent pageviews from list
    const recentEvents = await redis.lRange('recent:pageviews', 0, limit - 1);
    const parsed = recentEvents.map((e) => JSON.parse(e));

    res.json({ recent: parsed });
  } catch (error) {
    console.error('Error getting recent pageviews:', error);
    res.status(500).json({ error: 'Failed to get recent pageviews' });
  }
});

// Get summary statistics
router.get('/summary', async (req, res) => {
  try {
    if (!isRedisConnected()) {
      return res.json({
        totalPageviews: 0,
        totalClicks: 0,
        totalSearches: 0,
        uniquePages: 0,
        message: 'Redis not connected',
      });
    }

    const redis = getRedisClient();

    // Get all counters
    const pageviewKeys = await redis.keys('counter:pageview:*');
    const clickKeys = await redis.keys('counter:click:*');
    const searchKeys = await redis.keys('counter:search:*');

    // Sum up all pageviews
    let totalPageviews = 0;
    for (const key of pageviewKeys) {
      const count = await redis.get(key);
      totalPageviews += parseInt(count, 10);
    }

    // Sum up all clicks
    let totalClicks = 0;
    for (const key of clickKeys) {
      const count = await redis.get(key);
      totalClicks += parseInt(count, 10);
    }

    // Sum up all searches
    let totalSearches = 0;
    for (const key of searchKeys) {
      const count = await redis.get(key);
      totalSearches += parseInt(count, 10);
    }

    res.json({
      totalPageviews,
      totalClicks,
      totalSearches,
      uniquePages: pageviewKeys.length,
      uniqueElements: clickKeys.length,
      uniqueSearchQueries: searchKeys.length,
    });
  } catch (error) {
    console.error('Error getting summary:', error);
    res.status(500).json({ error: 'Failed to get summary' });
  }
});

// Get real-time metrics (last hour)
router.get('/realtime', async (req, res) => {
  try {
    if (!isRedisConnected()) {
      return res.json({ active: 0, message: 'Redis not connected' });
    }

    const redis = getRedisClient();

    // Get recent events from last hour
    const now = Date.now();
    const oneHourAgo = now - 60 * 60 * 1000;

    const recentEvents = await redis.lRange('recent:pageviews', 0, 99);
    const recentInHour = recentEvents
      .map((e) => JSON.parse(e))
      .filter((e) => new Date(e.timestamp).getTime() > oneHourAgo);

    // Count unique sessions in last hour
    const uniqueSessions = new Set(
      recentInHour.filter((e) => e.sessionId).map((e) => e.sessionId)
    );

    res.json({
      active: uniqueSessions.size,
      eventsLastHour: recentInHour.length,
    });
  } catch (error) {
    console.error('Error getting realtime metrics:', error);
    res.status(500).json({ error: 'Failed to get realtime metrics' });
  }
});

module.exports = router;
