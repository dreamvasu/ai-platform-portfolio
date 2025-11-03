"""
AI Blog Scraper - Fetch latest posts from AI company blogs
"""

import feedparser
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import re
import logging

logger = logging.getLogger(__name__)

BLOG_SOURCES = {
    'openai': {
        'type': 'rss',
        'url': 'https://openai.com/blog/rss.xml',
        'category': 'model-release',
        'display_name': 'OpenAI'
    },
    'google-ai': {
        'type': 'rss',
        'url': 'https://blog.google/technology/ai/rss/',
        'category': 'research',
        'display_name': 'Google AI'
    },
    'microsoft-ai': {
        'type': 'rss',
        'url': 'https://blogs.microsoft.com/ai/feed/',
        'category': 'products',
        'display_name': 'Microsoft AI'
    },
    'huggingface': {
        'type': 'rss',
        'url': 'https://huggingface.co/blog/feed.xml',
        'category': 'models',
        'display_name': 'HuggingFace'
    },
}


def clean_html(html_text: str) -> str:
    """Remove HTML tags and clean text"""
    if not html_text:
        return ""

    # Parse HTML
    soup = BeautifulSoup(html_text, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text and clean whitespace
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)

    # Limit length
    if len(text) > 500:
        text = text[:500] + "..."

    return text


def extract_tags(text: str) -> List[str]:
    """Extract relevant tags from title and content"""
    keywords = {
        'gpt': 'GPT',
        'claude': 'Claude',
        'gemini': 'Gemini',
        'llama': 'Llama',
        'mistral': 'Mistral',
        'llm': 'LLM',
        'model': 'AI Model',
        'training': 'Training',
        'fine-tuning': 'Fine-tuning',
        'benchmark': 'Benchmark',
        'deployment': 'Deployment',
        'api': 'API',
        'open source': 'Open Source',
        'multimodal': 'Multimodal',
        'vision': 'Vision',
        'embedding': 'Embeddings',
        'rag': 'RAG',
        'agents': 'AI Agents',
    }

    text_lower = text.lower()
    found_tags = []

    for keyword, tag in keywords.items():
        if keyword in text_lower:
            found_tags.append(tag)

    return found_tags[:5]  # Limit to 5 tags


def parse_date(date_str: str) -> datetime:
    """Parse various date formats"""
    try:
        # Try feedparser's struct_time format
        if hasattr(date_str, 'tm_year'):
            return datetime(*date_str[:6])

        # Try ISO format
        if isinstance(date_str, str):
            # Handle various ISO formats
            for fmt in ['%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                try:
                    return datetime.strptime(date_str[:19], fmt[:len(date_str)])
                except ValueError:
                    continue

    except Exception as e:
        logger.warning(f"Failed to parse date '{date_str}': {e}")

    # Default to now
    return datetime.now()


async def scrape_rss_feed(source_key: str, source_config: Dict, max_results: int = 10) -> List[Dict]:
    """Scrape blog posts from RSS feed"""
    posts = []

    try:
        logger.info(f"Scraping RSS feed: {source_config['display_name']}")

        # Fetch RSS feed
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(source_config['url'])
            response.raise_for_status()

        # Parse feed
        feed = feedparser.parse(response.content)

        # Extract posts
        for entry in feed.entries[:max_results]:
            try:
                # Get published date
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])
                else:
                    pub_date = datetime.now()

                # Get abstract/summary
                abstract = ""
                if hasattr(entry, 'summary'):
                    abstract = clean_html(entry.summary)
                elif hasattr(entry, 'description'):
                    abstract = clean_html(entry.description)

                # Get author
                author = ""
                if hasattr(entry, 'author'):
                    author = entry.author
                elif hasattr(entry, 'authors') and entry.authors:
                    author = entry.authors[0].get('name', '')

                # Build post
                post = {
                    'title': entry.title,
                    'url': entry.link,
                    'published_date': pub_date.isoformat(),
                    'abstract': abstract or entry.title,  # Fallback to title
                    'authors': author or source_config['display_name'],
                    'source': source_key,
                    'source_display': source_config['display_name'],
                    'category': source_config['category'],
                    'tags': extract_tags(entry.title + " " + abstract),
                    'relevance_score': 0.85  # Default high relevance for company blogs
                }

                posts.append(post)
                logger.debug(f"Extracted post: {post['title']}")

            except Exception as e:
                logger.error(f"Failed to parse entry from {source_key}: {e}")
                continue

        logger.info(f"Scraped {len(posts)} posts from {source_config['display_name']}")

    except Exception as e:
        logger.error(f"Failed to scrape {source_key}: {e}")

    return posts


async def scrape_all_blogs(max_per_source: int = 10) -> List[Dict]:
    """Scrape all configured blog sources"""
    all_posts = []

    for source_key, source_config in BLOG_SOURCES.items():
        if source_config['type'] == 'rss':
            posts = await scrape_rss_feed(source_key, source_config, max_per_source)
            all_posts.extend(posts)

    logger.info(f"Total posts scraped: {len(all_posts)}")
    return all_posts


async def scrape_specific_blog(source: str, max_results: int = 10) -> List[Dict]:
    """Scrape a specific blog source"""
    if source not in BLOG_SOURCES:
        raise ValueError(f"Unknown blog source: {source}. Available: {list(BLOG_SOURCES.keys())}")

    source_config = BLOG_SOURCES[source]

    if source_config['type'] == 'rss':
        return await scrape_rss_feed(source, source_config, max_results)

    return []
