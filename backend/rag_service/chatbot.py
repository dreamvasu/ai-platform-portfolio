"""
RAG Chatbot implementation using Google Vertex AI
Demonstrates hands-on GCP Generative AI experience
"""
from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration
import vertexai
import os
import requests
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

        # Define blog search tool
        search_blogs_func = FunctionDeclaration(
            name="search_blogs",
            description="Search Vasu's technical blog posts for information about Kubernetes, GCP, RAG, Docker, Terraform, CI/CD, monitoring, databases, etc.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find relevant blog posts"
                    }
                },
                "required": ["query"]
            }
        )

        blog_tool = Tool(function_declarations=[search_blogs_func])

        # Initialize Gemini model with tools (using Gemini 2.0)
        self.model = GenerativeModel("gemini-2.0-flash-exp", tools=[blog_tool])
        print(f"✅ Initialized Vertex AI Gemini 2.0 Flash with blog search tool (Project: {self.project_id})")

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

            # Generate answer using LLM with function calling
            answer, blog_sources = self._generate_answer_with_tools(question, context)

            # Prepare response
            response = {
                'answer': answer,
                'context_used': len(search_results['documents'])
            }

            if include_sources:
                sources = self._format_sources(search_results)
                # Add blog sources if any were used
                if blog_sources:
                    sources.extend(blog_sources)
                response['sources'] = sources

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

    def _search_blogs(self, query):
        """Search blog posts via API"""
        try:
            # Call the blog API
            api_url = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000/api')
            response = requests.get(f"{api_url}/papers/", params={"search": query})
            response.raise_for_status()

            results = response.json().get('results', [])

            # Format blog posts for context
            blog_context = []
            blog_sources = []

            for post in results[:3]:  # Top 3 most relevant
                blog_context.append(f"""
Blog Post: {post['title']}
Author: {post['authors']}
Published: {post['published_date']}
Tags: {', '.join(post['tags'])}

{post['abstract'][:800]}...
""")
                blog_sources.append({
                    'source': f"blog-{post['id']}",
                    'category': 'blog-post',
                    'title': post['title'],
                    'relevance_score': 0.9
                })

            return "\n\n---\n\n".join(blog_context), blog_sources

        except Exception as e:
            print(f"⚠️  Error searching blogs: {e}")
            return "", []

    def _generate_answer_with_tools(self, question, context):
        """Generate answer using Vertex AI Gemini with function calling"""
        prompt = f"""You are an AI assistant helping visitors learn about Vasu Kapoor's
journey to becoming an AI/ML Platform Engineer. You have access to:
1. Documentation about his 12-hour learning sprint (provided as context)
2. His technical blog posts (via search_blogs tool)

Your role:
- Answer questions based on the provided context
- If the question is about technical topics like Kubernetes, Docker, GCP, RAG, CI/CD, etc.,
  USE the search_blogs tool to find his blog posts about those topics
- Be specific and cite relevant details
- Keep answers concise but informative (2-4 paragraphs max)
- Use a friendly, professional tone

Context from documentation:

{context}

---

Question: {question}

Please provide a helpful answer. Use search_blogs if you need specific technical details from his blog posts."""

        # Start conversation with model
        chat = self.model.start_chat()

        # Send initial prompt
        response = chat.send_message(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 800,
            }
        )

        blog_sources = []

        # Check if model wants to use function
        function_call = response.candidates[0].content.parts[0].function_call if response.candidates[0].content.parts else None

        if function_call and function_call.name == "search_blogs":
            # Extract query argument
            query = function_call.args.get("query", "")
            print(f"🔍 Chatbot searching blogs for: {query}")

            # Actually search blogs
            blog_context, blog_sources = self._search_blogs(query)

            # Send function response back to model
            function_response = {
                "name": "search_blogs",
                "response": {
                    "content": blog_context if blog_context else "No relevant blog posts found."
                }
            }

            response = chat.send_message(
                function_response,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 800,
                }
            )

        return response.text, blog_sources

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
