"""
Vector Store implementation using ChromaDB
Stores document embeddings for RAG retrieval
"""
import chromadb
from chromadb.config import Settings
import os

class VectorStore:
    """ChromaDB-based vector store for portfolio documentation"""

    def __init__(self, persist_directory="./chroma_db"):
        """Initialize ChromaDB client and collection"""
        self.persist_directory = persist_directory

        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="portfolio_docs",
            metadata={"description": "Vasu's portfolio documentation and journey"}
        )

    def add_documents(self, documents, embeddings, metadatas, ids=None):
        """
        Add documents to the vector store

        Args:
            documents: List of text chunks
            embeddings: List of embedding vectors
            metadatas: List of metadata dicts
            ids: Optional list of document IDs
        """
        if ids is None:
            # Generate IDs if not provided
            existing_count = self.collection.count()
            ids = [f"doc_{existing_count + i}" for i in range(len(documents))]

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        print(f"✅ Added {len(documents)} documents to vector store")

    def search(self, query_embedding, k=5):
        """
        Search for similar documents

        Args:
            query_embedding: Query embedding vector
            k: Number of results to return

        Returns:
            Dictionary with documents, metadatas, and distances
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        return {
            'documents': results['documents'][0] if results['documents'] else [],
            'metadatas': results['metadatas'][0] if results['metadatas'] else [],
            'distances': results['distances'][0] if results['distances'] else []
        }

    def count(self):
        """Get total number of documents in store"""
        return self.collection.count()

    def clear(self):
        """Clear all documents from the collection"""
        self.client.delete_collection("portfolio_docs")
        self.collection = self.client.get_or_create_collection(
            name="portfolio_docs",
            metadata={"description": "Vasu's portfolio documentation and journey"}
        )
        print("✅ Cleared vector store")
