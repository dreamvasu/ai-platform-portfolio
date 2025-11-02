"""
Django management command to scrape ML/AI papers from various sources.

Usage:
    python manage.py scrape_papers --source arxiv --days 7
    python manage.py scrape_papers --source huggingface --days 30
    python manage.py scrape_papers --source all --days 7
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import Paper, ScraperJob


class Command(BaseCommand):
    help = 'Scrape ML/AI research papers from various sources'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='arxiv',
            choices=['arxiv', 'huggingface', 'paperswithcode', 'all'],
            help='Source to scrape from'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days to look back for papers'
        )
        parser.add_argument(
            '--max-results',
            type=int,
            default=50,
            help='Maximum number of results to fetch'
        )
        parser.add_argument(
            '--category',
            type=str,
            default='all',
            choices=['llm', 'cv', 'rag', 'mlops', 'training', 'inference', 'nlp', 'multimodal', 'all'],
            help='Category filter for papers'
        )

    def handle(self, *args, **options):
        source = options['source']
        days = options['days']
        max_results = options['max_results']
        category = options['category']

        self.stdout.write(self.style.SUCCESS(f'\n🔍 Starting paper scraper for source: {source}'))
        self.stdout.write(f'Looking back {days} days, max {max_results} results\n')

        if source == 'all':
            sources = ['arxiv', 'huggingface', 'paperswithcode']
        else:
            sources = [source]

        total_added = 0
        total_updated = 0

        for src in sources:
            if src == 'arxiv':
                added, updated = self.scrape_arxiv(days, max_results, category)
                total_added += added
                total_updated += updated
            elif src == 'huggingface':
                self.stdout.write(self.style.WARNING('Hugging Face scraper not implemented yet'))
            elif src == 'paperswithcode':
                self.stdout.write(self.style.WARNING('Papers with Code scraper not implemented yet'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Scraping complete!'))
        self.stdout.write(f'Papers added: {total_added}')
        self.stdout.write(f'Papers updated: {total_updated}\n')

    def scrape_arxiv(self, days, max_results, category_filter):
        """Scrape papers from arXiv API"""
        self.stdout.write(self.style.SUCCESS('\n📄 Scraping arXiv...'))

        # Create scraper job record
        job = ScraperJob.objects.create(
            source='arxiv',
            status='running'
        )

        try:
            # arXiv categories for AI/ML
            categories = [
                'cs.AI',  # Artificial Intelligence
                'cs.LG',  # Machine Learning
                'cs.CL',  # Computation and Language (NLP)
                'cs.CV',  # Computer Vision
                'cs.NE',  # Neural and Evolutionary Computing
            ]

            # Build search query
            category_query = ' OR '.join([f'cat:{cat}' for cat in categories])

            # Calculate date range
            from_date = (timezone.now() - timedelta(days=days)).strftime('%Y%m%d%H%M%S')

            # arXiv API parameters
            base_url = 'http://export.arxiv.org/api/query?'
            params = {
                'search_query': category_query,
                'start': 0,
                'max_results': max_results,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }

            url = base_url + urllib.parse.urlencode(params)

            self.stdout.write(f'Fetching from arXiv API...')

            # Fetch data
            with urllib.request.urlopen(url) as response:
                data = response.read()

            # Parse XML
            root = ET.fromstring(data)

            # Namespace for arXiv API
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }

            entries = root.findall('atom:entry', ns)

            self.stdout.write(f'Found {len(entries)} papers')

            papers_added = 0
            papers_updated = 0

            for entry in entries:
                try:
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
                    days_old = (timezone.now().date() - published_date).days
                    if days_old > days:
                        continue

                    # URLs
                    url = f'https://arxiv.org/abs/{arxiv_id}'
                    pdf_url = f'https://arxiv.org/pdf/{arxiv_id}.pdf'

                    # Categories
                    categories_elements = entry.findall('atom:category', ns)
                    arxiv_categories = [cat.get('term') for cat in categories_elements]

                    # Determine our category
                    category = self._determine_category(title, summary, arxiv_categories)

                    # Apply category filter
                    if category_filter != 'all' and category != category_filter:
                        continue

                    # Calculate relevance score
                    relevance_score = self._calculate_relevance(title, summary)

                    # Extract tags
                    tags = self._extract_tags(title, summary)

                    # Create or update paper
                    paper, created = Paper.objects.update_or_create(
                        source='arxiv',
                        source_id=arxiv_id,
                        defaults={
                            'title': title,
                            'abstract': summary,
                            'authors': authors,
                            'url': url,
                            'pdf_url': pdf_url,
                            'published_date': published_date,
                            'category': category,
                            'tags': tags,
                            'relevance_score': relevance_score,
                        }
                    )

                    if created:
                        papers_added += 1
                        self.stdout.write(self.style.SUCCESS(f'  ✓ Added: {title[:80]}...'))
                    else:
                        papers_updated += 1
                        self.stdout.write(f'  ↻ Updated: {title[:80]}...')

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Error processing entry: {str(e)}'))
                    continue

            # Update job record
            job.end_time = timezone.now()
            job.status = 'completed'
            job.papers_found = len(entries)
            job.papers_added = papers_added
            job.papers_updated = papers_updated
            job.log = f'Successfully scraped {len(entries)} papers from arXiv'
            job.save()

            self.stdout.write(self.style.SUCCESS(f'\n✅ arXiv scraping complete!'))
            self.stdout.write(f'Papers added: {papers_added}, updated: {papers_updated}')

            return papers_added, papers_updated

        except Exception as e:
            # Mark job as failed
            job.end_time = timezone.now()
            job.status = 'failed'
            job.errors = str(e)
            job.save()

            self.stdout.write(self.style.ERROR(f'\n❌ Error scraping arXiv: {str(e)}'))
            return 0, 0

    def _determine_category(self, title, abstract, arxiv_categories):
        """Determine paper category based on content"""
        text = (title + ' ' + abstract).lower()

        # Category keywords
        if any(kw in text for kw in ['large language model', 'llm', 'gpt', 'bert', 'transformer', 'language model']):
            return 'llm'
        elif any(kw in text for kw in ['retrieval augmented', 'rag', 'embedding', 'vector database', 'semantic search']):
            return 'rag'
        elif any(kw in text for kw in ['computer vision', 'image', 'visual', 'object detection', 'segmentation']):
            return 'cv'
        elif any(kw in text for kw in ['mlops', 'deployment', 'serving', 'inference', 'production', 'kubernetes']):
            return 'mlops'
        elif any(kw in text for kw in ['training', 'optimization', 'gradient', 'backpropagation']):
            return 'training'
        elif any(kw in text for kw in ['multimodal', 'vision-language', 'vlm', 'clip']):
            return 'multimodal'
        elif any(kw in text for kw in ['natural language', 'nlp', 'text']):
            return 'nlp'
        else:
            return 'nlm'  # Default

    def _calculate_relevance(self, title, abstract):
        """Calculate relevance score (0-1) based on keywords"""
        text = (title + ' ' + abstract).lower()

        # High relevance keywords for AI/ML Platform Engineering
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

    def _extract_tags(self, title, abstract):
        """Extract relevant tags from title and abstract"""
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
