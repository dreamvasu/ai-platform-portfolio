"""
Django management command to add source_id slugs to existing blog posts.

Usage:
    python manage.py fix_blog_slugs
    python manage.py fix_blog_slugs --dry-run
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from portfolio.models import Paper


class Command(BaseCommand):
    help = 'Add source_id slugs to blog posts that are missing them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        self.stdout.write(self.style.SUCCESS('\n🔧 Fixing blog post slugs...\n'))

        # Find blog posts without source_id (both "blog" and "blogs" sources)
        blogs_without_slug = Paper.objects.filter(
            source__in=['blog', 'blogs']
        ).filter(source_id__isnull=True) | Paper.objects.filter(
            source__in=['blog', 'blogs'],
            source_id=''
        )

        total = blogs_without_slug.count()
        self.stdout.write(f'Found {total} blog posts without slugs\n')

        if total == 0:
            self.stdout.write(self.style.SUCCESS('✅ All blog posts already have slugs!\n'))
            return

        updated = 0

        for blog in blogs_without_slug:
            # Generate slug from URL or title
            if blog.url:
                # Try to extract slug from URL
                parts = blog.url.rstrip('/').split('/')
                if len(parts) > 1 and parts[-1]:
                    slug = slugify(parts[-1])
                else:
                    slug = slugify(blog.title[:80])
            else:
                # Use title-based slug
                slug = slugify(blog.title[:80])

            # Ensure uniqueness
            base_slug = slug
            counter = 1
            while Paper.objects.filter(source_id=slug).exclude(id=blog.id).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            if dry_run:
                self.stdout.write(f'  [DRY RUN] Would update: {blog.title[:50]}')
                self.stdout.write(f'            Slug: {slug}\n')
            else:
                blog.source_id = slug
                blog.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated: {blog.title[:50]}'))
                self.stdout.write(f'    Slug: {slug}\n')

        if dry_run:
            self.stdout.write(self.style.WARNING(f'\n⚠️  DRY RUN: Would update {total} blog posts'))
            self.stdout.write('Run without --dry-run to apply changes\n')
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully updated {updated} blog posts!\n'))
