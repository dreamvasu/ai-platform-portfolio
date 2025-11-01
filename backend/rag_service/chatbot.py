"""
RAG Chatbot implementation using Google Vertex AI
Demonstrates hands-on GCP Generative AI experience
"""
from vertexai.generative_models import GenerativeModel
import vertexai
import os
from .vector_store import VectorStore
from .embeddings import EmbeddingGenerator

class PortfolioRAGChatbot:
    """
    RAG-powered chatbot that answers questions about Vasu's
    AI/ML platform engineering journey using Google Vertex AI
    """

    def __init__(self, vector_store=None, project_id=None, location="us-central1"):
        """
        Initialize RAG chatbot with Vertex AI

        Args:
            vector_store: VectorStore instance
            project_id: GCP project ID
            location: GCP region
        """
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        self.location = location

        # Initialize Vertex AI
        vertexai.init(project=self.project_id, location=self.location)

        # Initialize components
        self.vector_store = vector_store or VectorStore()
        self.embedding_gen = EmbeddingGenerator(project_id=self.project_id, location=self.location)

        # Initialize Gemini model for text generation (using Gemini 2.0)
        self.model = GenerativeModel("gemini-2.0-flash-exp")
        print(f"✅ Initialized Vertex AI Gemini 2.0 Flash (Project: {self.project_id})")

    def query(self, question, k=5, include_sources=True):
        """
        Answer a question using RAG

        Args:
            question: User's question
            k: Number of context documents to retrieve
            include_sources: Whether to include source documents in response

        Returns:
            Dictionary with answer, sources, and metadata
        """
        try:
            # Generate embedding for the question
            query_embedding = self.embedding_gen.generate_embedding(question)

            # Search vector store for relevant context
            search_results = self.vector_store.search(query_embedding, k=k)

            # Check if we have any results
            if not search_results['documents']:
                return {
                    'answer': "I don't have enough information to answer that question. Try asking about Vasu's learning journey, tech stack, or projects.",
                    'sources': [],
                    'context_used': 0
                }

            # Build context from retrieved documents
            context = self._build_context(search_results)

            # Generate answer using LLM
            answer = self._generate_answer(question, context)

            # Prepare response
            response = {
                'answer': answer,
                'context_used': len(search_results['documents'])
            }

            if include_sources:
                response['sources'] = self._format_sources(search_results)

            return response

        except Exception as e:
            print(f"❌ Error in RAG query: {e}")
            return {
                'answer': f"Sorry, I encountered an error: {str(e)}",
                'sources': [],
                'context_used': 0
            }

    def _build_context(self, search_results):
        """Build context string from search results"""
        context_parts = []

        for i, doc in enumerate(search_results['documents']):
            metadata = search_results['metadatas'][i]
            source = metadata.get('source', 'Unknown')

            context_parts.append(f"[Source: {source}]\n{doc}")

        return "\n\n---\n\n".join(context_parts)

    def _generate_answer(self, question, context):
        """Generate answer using Vertex AI Gemini"""
        prompt = f"""You are an AI assistant helping visitors learn about Vasu Kapoor's
journey to becoming an AI/ML Platform Engineer. You have access to documentation about his
12-hour learning sprint where he went from 65% match to 90% match for a Wipro role.

Your role:
- Answer questions based ONLY on the provided context below
- Be specific and cite relevant details from the journey
- If asked about technical implementations, provide concrete examples
- If the context doesn't contain the answer, say so honestly
- Keep answers concise but informative (2-4 paragraphs max)
- Use a friendly, professional tone
- Include relevant technologies and achievements when appropriate

DO NOT:
- Make up information not in the context
- Claim Vasu has experience he doesn't have
- Provide generic answers that could apply to anyone

---

Context from Vasu's documentation:

{context}

---

Question: {question}

Please provide a helpful answer based on the context above."""

        # Generate response with Gemini
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 500,
                "top_p": 0.9,
                "top_k": 40,
            }
        )

        return response.text

    def _format_sources(self, search_results):
        """Format source documents for response"""
        sources = []

        for i, metadata in enumerate(search_results['metadatas']):
            source = {
                'source': metadata.get('source', 'Unknown'),
                'category': metadata.get('category', 'general'),
                'chunk_id': metadata.get('chunk_id', 0),
                'relevance_score': 1 - search_results['distances'][i] if i < len(search_results['distances']) else 0
            }
            sources.append(source)

        return sources

    def get_suggested_questions(self):
        """Return suggested questions users can ask"""
        return [
            "How did Vasu learn Kubernetes?",
            "What's Vasu's experience with GCP?",
            "Tell me about the RAG system implementation",
            "What technologies did Vasu master in the sprint?",
            "Show me proof of deployments",
            "What challenges did Vasu face during the learning sprint?",
            "How did Vasu implement Infrastructure as Code?",
            "What's the architecture of this portfolio?",
        ]
