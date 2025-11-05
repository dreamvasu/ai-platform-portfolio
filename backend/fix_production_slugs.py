#!/usr/bin/env python3
"""
Direct script to fix blog slugs in production database.
Run with production DATABASE_URL environment variable.
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse
import re

def slugify(text):
    """Simple slugify function"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def generate_slug_from_url(url, title):
    """Generate slug from URL or title"""
    if url:
        parts = url.rstrip('/').split('/')
        if len(parts) > 1 and parts[-1]:
            slug = slugify(parts[-1])
            if len(slug) >= 10:
                return slug[:100]

    # Fallback to title
    return slugify(title[:80])

def fix_blog_slugs():
    """Fix blog post slugs in production database"""

    # Connect to production database
    db_url = "postgresql://django:OnmapREgkzsnD8vgGvZu72gwfwdjMjlk@34.31.185.136:5432/portfolio"

    print("🔗 Connecting to production database...")

    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        print("✅ Connected successfully\n")

        # Find blog posts without source_id
        cursor.execute("""
            SELECT id, title, url, source
            FROM portfolio_paper
            WHERE source IN ('blog', 'blogs')
            AND (source_id IS NULL OR source_id = '')
            ORDER BY id
        """)

        blogs = cursor.fetchall()
        total = len(blogs)

        print(f"📊 Found {total} blog posts without slugs\n")

        if total == 0:
            print("✅ All blog posts already have slugs!")
            return

        updated = 0

        for blog_id, title, url, source in blogs:
            # Generate slug
            slug = generate_slug_from_url(url, title)

            # Ensure uniqueness
            base_slug = slug
            counter = 1
            while True:
                cursor.execute(
                    "SELECT COUNT(*) FROM portfolio_paper WHERE source_id = %s AND id != %s",
                    (slug, blog_id)
                )
                if cursor.fetchone()[0] == 0:
                    break
                slug = f"{base_slug}-{counter}"
                counter += 1

            # Update the blog post
            cursor.execute(
                "UPDATE portfolio_paper SET source_id = %s WHERE id = %s",
                (slug, blog_id)
            )

            updated += 1
            print(f"  ✓ Updated ID {blog_id}: {title[:50]}")
            print(f"    Slug: {slug}\n")

        # Commit changes
        conn.commit()

        print(f"\n✅ Successfully updated {updated} blog posts!")

        # Verify
        cursor.execute("""
            SELECT COUNT(*)
            FROM portfolio_paper
            WHERE source IN ('blog', 'blogs')
            AND (source_id IS NULL OR source_id = '')
        """)
        remaining = cursor.fetchone()[0]

        print(f"📊 Remaining without slugs: {remaining}\n")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_blog_slugs()
