#!/usr/bin/env python
"""
Document ingestion script for RAG system
Loads markdown documentation and populates vector store
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from rag_service.vector_store import VectorStore
from rag_service.embeddings import EmbeddingGenerator
from rag_service.document_processor import DocumentProcessor
from portfolio.models import Paper

def fetch_blog_posts_as_documents():
    """Fetch blog posts from database and convert to document format"""
    documents = []

    try:
        blog_posts = Paper.objects.all()
        print(f"  📝 Found {blog_posts.count()} blog posts in database")

        for post in blog_posts:
            # Format blog post as markdown document
            doc_content = f"""# {post.title}

**Author:** {post.authors}
**Published:** {post.published_date}
**Category:** {post.get_category_display()}
**Tags:** {', '.join(post.tags)}

## Content

{post.abstract}

**Source:** Blog post from portfolio
**URL:** /blog/{post.id}
"""
            documents.append({
                'content': doc_content,
                'source': f'blog-{post.source_id}',
                'category': 'blog-post',
                'title': post.title
            })
            print(f"    ✓ Loaded blog post: {post.title[:60]}...")
    except Exception as e:
        print(f"  ⚠️  Error fetching blog posts: {e}")

    return documents

def main():
    print("=" * 60)
    print("🚀 STARTING DOCUMENT INGESTION FOR RAG SYSTEM")
    print("   Using Google Vertex AI Embeddings")
    print("=" * 60)

    # Check for GCP credentials
    if not os.getenv('GOOGLE_CLOUD_PROJECT'):
        print("\n❌ ERROR: GOOGLE_CLOUD_PROJECT environment variable not set")
        print("Please set it with: export GOOGLE_CLOUD_PROJECT='your-project-id'")
        print("Also ensure GOOGLE_APPLICATION_CREDENTIALS is set to your service account key")
        return

    # Initialize components
    print("\n📦 Initializing components...")
    vector_store = VectorStore(persist_directory="./chroma_db")
    embedding_gen = EmbeddingGenerator()
    doc_processor = DocumentProcessor(chunk_size=500, overlap=50)

    # Clear existing data (optional - comment out if you want to keep existing data)
    print("\n🗑️  Clearing existing vector store...")
    vector_store.clear()

    # Define document directories to ingest
    doc_directories = [
        '../docs/planning',      # Planning documents
        '../docs/journey',       # Journey entries (if they exist)
        '../docs/technical',     # Technical docs (if they exist)
        '../docs/case-studies',  # Production case studies
        '.',                     # Root directory (CLAUDE.md, README.md)
    ]

    # Load all documents
    print("\n📚 Loading markdown documents...")
    all_documents = []

    for directory in doc_directories:
        if os.path.exists(directory):
            print(f"\n  Loading from: {directory}")
            docs = doc_processor.load_markdown_files(directory)
            all_documents.extend(docs)
        else:
            print(f"  ⚠️  Directory not found: {directory}")

    # Load blog posts from database
    print("\n📰 Loading blog posts from database...")
    blog_docs = fetch_blog_posts_as_documents()
    all_documents.extend(blog_docs)

    if not all_documents:
        print("\n❌ No documents found to ingest!")
        return

    # Process documents into chunks
    print("\n✂️  Processing documents into chunks...")
    chunks, metadatas = doc_processor.process_documents(all_documents)

    # Generate embeddings
    print(f"\n🧮 Generating embeddings for {len(chunks)} chunks...")
    print("  (This may take a minute...)")
    embeddings = embedding_gen.generate_embeddings(chunks)

    # Add to vector store
    print("\n💾 Adding to vector store...")
    vector_store.add_documents(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    # Summary
    print("\n" + "=" * 60)
    print("🎉 DOCUMENT INGESTION COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   - Markdown documents: {len([d for d in all_documents if 'blog-post' not in d.get('category', '')])}")
    print(f"   - Blog posts: {len([d for d in all_documents if d.get('category') == 'blog-post'])}")
    print(f"   - Total source documents: {len(all_documents)}")
    print(f"   - Text chunks: {len(chunks)}")
    print(f"   - Vector store size: {vector_store.count()} documents")
    print(f"\n✅ RAG system is ready to answer questions!")
    print(f"   The chatbot can now reference:")
    print(f"   - Portfolio documentation")
    print(f"   - Technical blog posts")
    print(f"   - Case studies")
    print("\nNext steps:")
    print("  1. Run Django server: python manage.py runserver")
    print("  2. Test chatbot at: http://127.0.0.1:8000/api/chatbot/")
    print("  3. Ask about blog posts: 'Tell me about Kubernetes deployment'")


if __name__ == "__main__":
    main()
