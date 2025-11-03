# AI Blog Scraper Implementation Plan

## Overview

**Goal:** Repurpose the Papers scraper to show latest AI company blogs (model releases, research, benchmarks)

**Why:** Shows you stay current with AI industry developments - way more relevant than academic papers for an ML Platform Engineer role.

---

## Current Infrastructure (Already Built)

✅ **Paper Scraper Service** (FastAPI, deployed on Cloud Run)
- Location: `backend/services/scraper/`
- Endpoint: https://paper-scraper-434831039257.us-central1.run.app
- Webhook integration to Django backend

✅ **Django Paper Model**
- Fields: title, abstract, authors, url, source, published_date, category, tags, relevance_score
- API: `/api/papers/`
- Pagination, filtering, sorting built-in

✅ **Frontend Papers Page**
- Component: `frontend/src/pages/Papers.jsx`
- Features: Category filtering, sorting, search
- Ready to display blog posts

---

## What Needs to Change

### 1. Backend Scraper Service

**Add RSS/Blog Scrapers:**

```python
# backend/services/scraper/app/scrapers/blog_scraper.py

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BLOG_SOURCES = {
    'openai': {
        'type': 'rss',
        'url': 'https://openai.com/blog/rss.xml',
        'category': 'model-release'
    },
    'anthropic': {
        'type': 'web',
        'url': 'https://www.anthropic.com/news',
        'category': 'model-release'
    },
    'google-ai': {
        'type': 'rss',
        'url': 'https://blog.google/technology/ai/rss/',
        'category': 'research'
    },
    'meta-ai': {
        'type': 'web',
        'url': 'https://ai.meta.com/blog/',
        'category': 'research'
    },
    'huggingface': {
        'type': 'rss',
        'url': 'https://huggingface.co/blog/feed.xml',
        'category': 'models'
    },
    'microsoft-ai': {
        'type': 'rss',
        'url': 'https://blogs.microsoft.com/ai/feed/',
        'category': 'products'
    }
}

async def scrape_rss_feed(source_config):
    """Scrape blog posts from RSS feed"""
    feed = feedparser.parse(source_config['url'])
    posts = []

    for entry in feed.entries[:10]:  # Latest 10 posts
        post = {
            'title': entry.title,
            'url': entry.link,
            'published_date': datetime(*entry.published_parsed[:6]),
            'abstract': clean_html(entry.summary),
            'source': source_config['name'],
            'category': source_config['category'],
            'tags': extract_tags(entry.title + entry.summary)
        }
        posts.append(post)

    return posts

async def scrape_web_blog(source_config):
    """Scrape blog posts from web page"""
    response = requests.get(source_config['url'])
    soup = BeautifulSoup(response.content, 'html.parser')

    # Custom parsing logic per site
    # ...

    return posts
```

**Update Main Scraper:**
```python
# backend/services/scraper/app/main.py

@app.post("/scrape")
async def trigger_scrape(request: ScrapeRequest):
    if request.source == "blogs":
        # Scrape all AI company blogs
        results = await scrape_all_blogs()
    elif request.source == "arxiv":
        # Keep arXiv scraper for backwards compat
        results = await scrape_arxiv()
```

### 2. Django Backend

**Update Paper Model Categories:**

```python
# backend/portfolio/models.py

CATEGORY_CHOICES = [
    ('model-release', 'Model Release'),      # GPT-4o, Claude 3.5, Llama 3
    ('research', 'Research & Benchmarks'),   # New papers, benchmark results
    ('products', 'Product Updates'),         # Copilot, ChatGPT features
    ('models', 'Model Hub'),                 # HuggingFace trending
    ('infrastructure', 'ML Infrastructure'), # MLOps, serving, deployment
    ('industry', 'Industry News'),           # Company announcements
]

SOURCE_CHOICES = [
    ('openai', 'OpenAI'),
    ('anthropic', 'Anthropic'),
    ('google', 'Google AI'),
    ('meta', 'Meta AI'),
    ('microsoft', 'Microsoft AI'),
    ('huggingface', 'HuggingFace'),
    ('stability', 'Stability AI'),
    ('cohere', 'Cohere'),
    ('mistral', 'Mistral AI'),
]
```

**Add Management Command:**
```python
# backend/portfolio/management/commands/scrape_blogs.py

from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Trigger blog scraping
        response = requests.post(
            'http://localhost:8001/scrape',
            json={'source': 'blogs', 'max_results': 50}
        )
        self.stdout.write(f'Scraped {response.json()["papers_added"]} blogs')
```

### 3. Frontend Updates

**Rename & Rebrand:**

```jsx
// frontend/src/pages/Papers.jsx → AIUpdates.jsx

<h1>AI Industry Updates</h1>
<p>Latest model releases, research breakthroughs, and AI company announcements</p>

// Update categories
const categories = [
  { id: 'all', label: 'All Updates' },
  { id: 'model-release', label: 'New Models', icon: '🚀' },
  { id: 'research', label: 'Research', icon: '🔬' },
  { id: 'products', label: 'Products', icon: '💼' },
  { id: 'models', label: 'Model Hub', icon: '🤗' },
]

// Update display
<div className="blog-post">
  <div className="flex items-center gap-2 mb-2">
    <img src={getSourceLogo(post.source)} className="w-6 h-6" />
    <span className="font-medium">{post.source_display}</span>
    <span className="text-gray-500">•</span>
    <span className="text-sm text-gray-500">
      {formatDate(post.published_date)}
    </span>
  </div>
  <h3 className="text-xl font-bold mb-2">{post.title}</h3>
  <p className="text-gray-600 mb-4">{post.abstract}</p>
  <a href={post.url} className="text-blue-600 hover:text-blue-800">
    Read on {post.source_display} →
  </a>
</div>
```

**Update Navigation:**
```jsx
// frontend/src/components/layout/Navbar.jsx

<Link to="/ai-updates">AI Updates</Link>
```

---

## Implementation Steps

### Phase 1: Backend Scraper (30 mins)
1. ✅ Add `feedparser` to requirements.txt
2. ✅ Create `blog_scraper.py` with RSS/web scrapers
3. ✅ Update main.py to support blog scraping
4. ✅ Test locally: scrape OpenAI, Anthropic, Google blogs
5. ✅ Deploy to Cloud Run

### Phase 2: Django Updates (15 mins)
1. ✅ Update Paper model categories (migration)
2. ✅ Update serializers with new display names
3. ✅ Test API returns blog posts correctly
4. ✅ Deploy backend to Cloud Run

### Phase 3: Frontend Rebrand (15 mins)
1. ✅ Rename Papers.jsx → AIUpdates.jsx
2. ✅ Update categories and filtering
3. ✅ Add company logos/icons
4. ✅ Update navigation
5. ✅ Deploy to Vercel

### Phase 4: Testing (10 mins)
1. ✅ Trigger blog scraping
2. ✅ Verify 20-30 posts appear
3. ✅ Check filtering works
4. ✅ Verify links work

**Total Time:** ~70 minutes

---

## Sample Blog Posts We'll Get

**OpenAI:**
- "Introducing GPT-4o: our fastest and most affordable flagship model"
- "Improving o1-preview's safety and security"

**Anthropic:**
- "Introducing Claude 3.5 Sonnet"
- "Evaluating language model safety & security"

**Google AI:**
- "Gemini 1.5 Pro: Our next-generation model"
- "Project IDX: AI-powered workspace"

**Meta AI:**
- "Llama 3: The most capable openly available LLM"
- "Segment Anything Model 2"

**HuggingFace:**
- "Introducing Transformers 4.40"
- "New models trending this week"

---

## Benefits

**For Your Portfolio:**
- ✅ Shows you follow industry trends
- ✅ Demonstrates awareness of latest models/tools
- ✅ Proves you evaluate new tech for platform decisions
- ✅ Much more relevant than academic papers

**For Interviews:**
- "I built a system to track AI company announcements"
- "I stay current with model releases - here's my feed"
- "When GPT-4o came out, I evaluated it for our platform"

**SEO & Traffic:**
- People searching "latest AI models" find your site
- Demonstrates thought leadership
- More valuable content than academic research

---

## Alternative: Manual Curation (10 mins)

If we want to ship faster, we can:
1. Manually add 10-15 important blog posts to database
2. Ship the frontend now
3. Build scraper automation later

**Pros:** Faster to production
**Cons:** Need manual updates

**Recommendation:** Build the scraper - it's only 1 hour and provides automatic updates.

---

## Success Metrics

- ✅ 30+ blog posts scraped automatically
- ✅ Updated daily/weekly via cron job
- ✅ Categories accurately reflect content
- ✅ All links work and point to original sources
- ✅ Page looks professional and well-designed

---

**Status:** Ready to implement
**Next Step:** Phase 1 - Build blog scrapers
