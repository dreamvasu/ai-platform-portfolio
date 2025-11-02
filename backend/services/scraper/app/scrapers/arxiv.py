"""
arXiv API scraper
Migrated from Django management command - tested and working
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

from app.models import PaperData, SourceType, CategoryType

logger = logging.getLogger(__name__)


class ArxivScraper:
    """Scraper for arXiv papers"""

    def __init__(self, base_url: str = "http://export.arxiv.org/api/query"):
        self.base_url = base_url
        self.categories = [
            'cs.AI',  # Artificial Intelligence
            'cs.LG',  # Machine Learning
            'cs.CL',  # Computation and Language (NLP)
            'cs.CV',  # Computer Vision
            'cs.NE',  # Neural and Evolutionary Computing
        ]

    async def scrape(
        self,
        days: int = 7,
        max_results: int = 50,
        category_filter: Optional[str] = None
    ) -> List[PaperData]:
        """
        Scrape papers from arXiv

        Args:
            days: Look back N days
            max_results: Maximum number of results
            category_filter: Optional category filter

        Returns:
            List of PaperData objects
        """
        logger.info(f"Starting arXiv scrape: days={days}, max_results={max_results}")

        try:
            # Build search query
            category_query = ' OR '.join([f'cat:{cat}' for cat in self.categories])

            # arXiv API parameters
            params = {
                'search_query': category_query,
                'start': 0,
                'max_results': max_results,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }

            url = self.base_url + '?' + urllib.parse.urlencode(params)
            logger.info(f"Fetching from arXiv API: {url}")

            # Fetch data (synchronous for now - works reliably)
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read()

            # Parse XML
            root = ET.fromstring(data)

            # Namespace for arXiv API
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }

            entries = root.findall('atom:entry', ns)
            logger.info(f"Found {len(entries)} papers from arXiv")

            papers = []
            cutoff_date = datetime.now().date() - timedelta(days=days)

            for entry in entries:
                try:
                    paper = self._parse_entry(entry, ns, cutoff_date, category_filter)
                    if paper:
                        papers.append(paper)
                except Exception as e:
                    logger.warning(f"Error parsing entry: {str(e)}")
                    continue

            logger.info(f"Successfully parsed {len(papers)} papers")
            return papers

        except Exception as e:
            logger.error(f"Error scraping arXiv: {str(e)}")
            raise

    def _parse_entry(
        self,
        entry: ET.Element,
        ns: Dict[str, str],
        cutoff_date: datetime.date,
        category_filter: Optional[str]
    ) -> Optional[PaperData]:
        """Parse a single arXiv entry"""

        # Extract paper details
        arxiv_id = entry.find('atom:id', ns).text.split('/abs/')[-1]
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')

        # Authors
        authors_elements = entry.findall('atom:author', ns)
        authors = ', '.join([
            author.find('atom:name', ns).text
            for author in authors_elements
        ])

        # Published date
        published = entry.find('atom:published', ns).text
        published_date = datetime.strptime(published[:10], '%Y-%m-%d').date()

        # Skip if too old
        if published_date < cutoff_date:
            return None

        # URLs
        url = f'https://arxiv.org/abs/{arxiv_id}'
        pdf_url = f'https://arxiv.org/pdf/{arxiv_id}.pdf'

        # Categories
        categories_elements = entry.findall('atom:category', ns)
        arxiv_categories = [cat.get('term') for cat in categories_elements]

        # Determine our category
        category = self._determine_category(title, summary, arxiv_categories)

        # Apply category filter
        if category_filter and category != category_filter:
            return None

        # Calculate relevance score
        relevance_score = self._calculate_relevance(title, summary)

        # Extract tags
        tags = self._extract_tags(title, summary)

        return PaperData(
            title=title[:500],  # Truncate if needed
            abstract=summary,
            authors=authors,
            source=SourceType.ARXIV,
            source_id=arxiv_id,
            url=url,
            pdf_url=pdf_url,
            published_date=published_date,
            category=category,
            tags=tags,
            relevance_score=relevance_score,
            citation_count=0  # arXiv doesn't provide this
        )

    def _determine_category(
        self,
        title: str,
        abstract: str,
        arxiv_categories: List[str]
    ) -> CategoryType:
        """Determine paper category based on content"""
        text = (title + ' ' + abstract).lower()

        # Category keywords (same logic as Django command)
        if any(kw in text for kw in ['large language model', 'llm', 'gpt', 'bert', 'transformer', 'language model']):
            return CategoryType.LLM
        elif any(kw in text for kw in ['retrieval augmented', 'rag', 'embedding', 'vector database', 'semantic search']):
            return CategoryType.RAG
        elif any(kw in text for kw in ['computer vision', 'image', 'visual', 'object detection', 'segmentation']):
            return CategoryType.CV
        elif any(kw in text for kw in ['mlops', 'deployment', 'serving', 'inference', 'production', 'kubernetes']):
            return CategoryType.MLOPS
        elif any(kw in text for kw in ['training', 'optimization', 'gradient', 'backpropagation']):
            return CategoryType.TRAINING
        elif any(kw in text for kw in ['multimodal', 'vision-language', 'vlm', 'clip']):
            return CategoryType.MULTIMODAL
        elif any(kw in text for kw in ['natural language', 'nlp', 'text']):
            return CategoryType.NLP
        else:
            return CategoryType.NLP  # Default

    def _calculate_relevance(self, title: str, abstract: str) -> float:
        """Calculate relevance score (0-1)"""
        text = (title + ' ' + abstract).lower()

        # High relevance keywords
        high_keywords = [
            'large language model', 'llm', 'rag', 'retrieval augmented',
            'embedding', 'mlops', 'deployment', 'kubernetes', 'inference',
            'serving', 'optimization', 'distributed training'
        ]

        medium_keywords = [
            'transformer', 'attention', 'neural network', 'deep learning',
            'machine learning', 'artificial intelligence'
        ]

        score = 0.5  # Base score

        # Count keyword matches
        high_matches = sum(1 for kw in high_keywords if kw in text)
        medium_matches = sum(1 for kw in medium_keywords if kw in text)

        # Adjust score
        score += min(high_matches * 0.1, 0.4)
        score += min(medium_matches * 0.05, 0.1)

        return min(score, 1.0)

    def _extract_tags(self, title: str, abstract: str) -> List[str]:
        """Extract relevant tags"""
        text = (title + ' ' + abstract).lower()

        tag_keywords = {
            'transformers': ['transformer', 'attention mechanism'],
            'llm': ['large language model', 'llm'],
            'rag': ['retrieval augmented', 'rag'],
            'embeddings': ['embedding', 'vector'],
            'mlops': ['mlops', 'deployment', 'production'],
            'kubernetes': ['kubernetes', 'k8s'],
            'distributed': ['distributed', 'parallel'],
            'optimization': ['optimization', 'gradient descent'],
            'fine-tuning': ['fine-tuning', 'fine tuning', 'transfer learning'],
            'inference': ['inference', 'serving'],
            'quantization': ['quantization', 'compression'],
            'prompt-engineering': ['prompt engineering', 'prompt'],
        }

        tags = []
        for tag, keywords in tag_keywords.items():
            if any(kw in text for kw in keywords):
                tags.append(tag)

        return tags[:10]  # Limit to 10 tags
