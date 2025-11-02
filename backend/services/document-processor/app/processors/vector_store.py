# ChromaDB Vector Store Integration
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from app.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB vector store for document embeddings"""

    def __init__(self):
        self.client = None
        self.collection = None
        self._initialize()

    def _initialize(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create ChromaDB client with persistent storage
            self.client = chromadb.Client(
                Settings(
                    persist_directory=settings.chromadb_persist_directory,
                    anonymized_telemetry=False,
                )
            )

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="portfolio_documents",
                metadata={"description": "Portfolio documents and code for RAG"},
            )

            logger.info(
                f"ChromaDB initialized: {self.collection.count()} documents in collection"
            )

        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            # Don't raise - allow service to start without ChromaDB
            self.client = None
            self.collection = None

    def add_documents(
        self,
        chunks: List[Dict[str, Any]],
        embeddings: Optional[List[List[float]]] = None,
    ) -> int:
        """Add document chunks to vector store"""
        if not self.collection:
            logger.warning("ChromaDB not initialized, skipping add_documents")
            return 0

        try:
            # Prepare data for ChromaDB
            ids = []
            documents = []
            metadatas = []

            for i, chunk in enumerate(chunks):
                chunk_id = f"chunk_{chunk.get('metadata', {}).get('chunk_index', i)}"
                ids.append(chunk_id)
                documents.append(chunk["text"])
                metadatas.append(chunk.get("metadata", {}))

            # Add to collection
            if embeddings:
                self.collection.add(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas,
                    embeddings=embeddings,
                )
            else:
                # Let ChromaDB generate embeddings
                self.collection.add(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas,
                )

            logger.info(f"Added {len(chunks)} chunks to vector store")
            return len(chunks)

        except Exception as e:
            logger.error(f"Failed to add documents to vector store: {e}")
            raise

    def query(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Query vector store for relevant documents"""
        if not self.collection:
            logger.warning("ChromaDB not initialized, returning empty results")
            return []

        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where,
            )

            # Format results
            formatted_results = []
            if results["ids"] and len(results["ids"]) > 0:
                for i in range(len(results["ids"][0])):
                    formatted_results.append(
                        {
                            "id": results["ids"][0][i],
                            "text": results["documents"][0][i],
                            "metadata": results["metadatas"][0][i],
                            "distance": results["distances"][0][i]
                            if "distances" in results
                            else None,
                        }
                    )

            logger.info(f"Query returned {len(formatted_results)} results")
            return formatted_results

        except Exception as e:
            logger.error(f"Query failed: {e}")
            return []

    def delete_by_metadata(self, where: Dict[str, Any]) -> int:
        """Delete documents by metadata filter"""
        if not self.collection:
            logger.warning("ChromaDB not initialized, skipping delete")
            return 0

        try:
            # Query to find IDs matching the filter
            results = self.collection.get(where=where)
            if results["ids"]:
                self.collection.delete(ids=results["ids"])
                logger.info(f"Deleted {len(results['ids'])} documents")
                return len(results["ids"])
            return 0

        except Exception as e:
            logger.error(f"Delete failed: {e}")
            raise

    def count(self) -> int:
        """Get total document count"""
        if not self.collection:
            return 0
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Count failed: {e}")
            return 0

    def reset(self):
        """Reset (clear) the collection"""
        if not self.collection:
            logger.warning("ChromaDB not initialized, skipping reset")
            return

        try:
            # Delete all documents
            self.client.delete_collection(name="portfolio_documents")
            # Recreate collection
            self.collection = self.client.create_collection(
                name="portfolio_documents",
                metadata={"description": "Portfolio documents and code for RAG"},
            )
            logger.info("Vector store reset successfully")

        except Exception as e:
            logger.error(f"Reset failed: {e}")
            raise


# Singleton instance
vector_store = VectorStore()
