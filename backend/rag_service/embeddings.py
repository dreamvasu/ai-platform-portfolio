"""
Embedding generation using Google Vertex AI
Demonstrates hands-on GCP AI Platform experience
"""
from vertexai.language_models import TextEmbeddingModel
import vertexai
import os

class EmbeddingGenerator:
    """Generate embeddings using Google Vertex AI Text Embeddings"""

    def __init__(self, project_id=None, location="us-central1"):
        """
        Initialize Vertex AI client

        Args:
            project_id: GCP project ID (defaults to GOOGLE_CLOUD_PROJECT env var)
            location: GCP region for Vertex AI
        """
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        self.location = location

        # Initialize Vertex AI
        vertexai.init(project=self.project_id, location=self.location)

        # Load the text embedding model (using latest version)
        self.model = TextEmbeddingModel.from_pretrained("text-embedding-004")
        print(f"✅ Initialized Vertex AI Embeddings (Project: {self.project_id})")

    def generate_embedding(self, text):
        """
        Generate embedding for a single text using Vertex AI

        Args:
            text: Input text string

        Returns:
            Embedding vector (list of floats)
        """
        embeddings = self.model.get_embeddings([text])
        return embeddings[0].values

    def generate_embeddings(self, texts, batch_size=5):
        """
        Generate embeddings for multiple texts in batch using Vertex AI

        Args:
            texts: List of text strings
            batch_size: Number of texts per batch (Vertex AI limit is 250)

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        # Process in batches (Vertex AI has a limit of 250 texts per request)
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.model.get_embeddings(batch)
            all_embeddings.extend([emb.values for emb in batch_embeddings])

            if len(texts) > batch_size:
                print(f"  Processed {min(i + batch_size, len(texts))}/{len(texts)} embeddings...")

        print(f"✅ Generated {len(all_embeddings)} embeddings with Vertex AI")
        return all_embeddings
