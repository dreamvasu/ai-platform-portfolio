#!/usr/bin/env python
"""
Simple script to add blog posts to existing vector store
Fetches blogs from production API
"""
import os
import requests
from rag_service.vector_store import VectorStore
from rag_service.embeddings import EmbeddingGenerator
from rag_service.document_processor import DocumentProcessor

def main():
    print("=" * 60)
    print("🚀 ADDING BLOG POSTS TO VECTOR STORE")
    print("=" * 60)

    # Fetch blog posts from production API
    print("\n📰 Fetching blog posts from production API...")
    api_url = "https://portfolio-backend-eituuhu2yq-uc.a.run.app/api/papers/"
    response = requests.get(api_url)
    response.raise_for_status()
    blog_posts = response.json().get('results', [])
    print(f"  📝 Found {len(blog_posts)} blog posts")

    # Convert to documents (tuples of content and metadata)
    documents = []
    for post in blog_posts:
        doc_content = f"""# {post['title']}

**Author:** {post['authors']}
**Published:** {post['published_date']}
**Category:** {post['category']}
**Tags:** {', '.join(post['tags'])}

## Content

{post['abstract']}

**Source:** Blog post from portfolio
**URL:** /blog/{post['id']}
"""
        metadata = {
            'source': f"blog-{post['id']}",
            'category': 'blog-post',
            'title': post['title']
        }
        documents.append((doc_content, metadata))
        print(f"    ✓ Loaded: {post['title'][:60]}...")

    if not documents:
        print("\n❌ No blog posts found!")
        return

    # Initialize components
    print("\n📦 Initializing components...")
    vector_store = VectorStore(persist_directory="./chroma_db")
    embedding_gen = EmbeddingGenerator()
    doc_processor = DocumentProcessor(chunk_size=500, overlap=50)

    # Process documents into chunks
    print("\n✂️  Processing blog posts into chunks...")
    chunks, metadatas = doc_processor.process_documents(documents)

    # Generate embeddings
    print(f"\n🧮 Generating embeddings for {len(chunks)} chunks...")
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
    print("🎉 BLOG POSTS ADDED TO VECTOR STORE!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   - Blog posts added: {len(documents)}")
    print(f"   - Text chunks: {len(chunks)}")
    print(f"   - Total vector store size: {vector_store.count()} documents")
    print(f"\n✅ Chatbot can now reference blog posts!")

if __name__ == "__main__":
    main()
