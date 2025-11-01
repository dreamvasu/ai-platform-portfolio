# Backend & RAG Implementation

## RAG Chatbot Architecture

### Knowledge Base Structure

```python
# docs/knowledge_base.py

KNOWLEDGE_SOURCES = [
    {
        "type": "markdown",
        "path": "docs/journey/",
        "metadata": {
            "category": "journey",
            "tags": ["learning", "timeline", "sprint"]
        }
    },
    {
        "type": "markdown",
        "path": "docs/technical/",
        "metadata": {
            "category": "technical",
            "tags": ["architecture", "api", "deployment"]
        }
    },
    {
        "type": "code",
        "path": "backend/",
        "metadata": {
            "category": "code",
            "tags": ["django", "python", "api"]
        }
    },
    {
        "type": "code",
        "path": "frontend/src/",
        "metadata": {
            "category": "code",
            "tags": ["react", "javascript", "frontend"]
        }
    },
    {
        "type": "infrastructure",
        "path": "infrastructure/",
        "metadata": {
            "category": "infrastructure",
            "tags": ["terraform", "kubernetes", "deployment"]
        }
    }
]
```

### RAG Service Architecture

```python
# backend/rag_service/chatbot.py

class PortfolioChatbot:
    """
    RAG-powered chatbot that answers questions about
    Vasu's learning journey and technical implementations.
    """

    def __init__(self):
        self.vector_store = ChromaDB()
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4")

    def ingest_documentation(self):
        """Load all documentation into vector store"""
        for source in KNOWLEDGE_SOURCES:
            documents = self.load_documents(source)
            chunks = self.chunk_documents(documents)
            embeddings = self.embeddings.embed_documents(chunks)
            self.vector_store.add(chunks, embeddings, source.metadata)

    def query(self, question: str, context: dict = None):
        """Answer questions using RAG"""
        # Get relevant context
        relevant_docs = self.vector_store.similarity_search(question, k=5)

        # Build prompt
        prompt = self.build_prompt(question, relevant_docs, context)

        # Generate answer
        response = self.llm(prompt)

        # Add sources
        return {
            "answer": response,
            "sources": [doc.metadata for doc in relevant_docs],
            "confidence": self.calculate_confidence(relevant_docs)
        }

    def build_prompt(self, question, docs, context):
        """Build RAG prompt"""
        return f"""
        You are an AI assistant helping visitors learn about Vasu Kapoor's
        journey to becoming an AI/ML Platform Engineer.

        Context from Vasu's documentation:
        {self.format_docs(docs)}

        Question: {question}

        Instructions:
        - Answer based ONLY on the provided context
        - Be specific and cite relevant parts of the journey
        - Include links to relevant GitHub repos or pages
        - If you don't know, say so
        - Keep answers concise but informative

        Answer:
        """
```

### Sample Chatbot Interactions

```
User: "How did Vasu learn Kubernetes?"

Bot: "Vasu learned Kubernetes during hours 1-2 of his 12-hour sprint.
He focused on core concepts: Pods, Deployments, Services, and HPA.
His approach was hands-on - he built a working RAG API deployment
with autoscaling and load balancing.

Key achievements:
✅ Deployed microservice to Minikube
✅ Implemented horizontal pod autoscaling
✅ Set up ingress and load balancing
✅ Wrote K8s manifests from scratch

You can see his implementation here: [GitHub link]
And read his detailed journey here: [Journey page link]"

---

User: "What's Vasu's experience with GCP?"

Bot: "Vasu has production experience with Azure and recently gained
hands-on GCP experience during his 12-hour sprint.

GCP technologies he used:
✅ Cloud Run (serverless containers)
✅ Vertex AI (managed ML services)
✅ Cloud SQL (managed database)
✅ Cloud Build (CI/CD)

He deployed 2 production services to GCP:
1. Django backend API (Cloud Run)
2. RAG chatbot service (Cloud Run)

Both are live and auto-scaling. Try the demo: [Live URL]
Architecture details: [GCP Deep Dive page]"
```

## Implementation Code Examples

### Vector Store Setup

```python
# backend/rag_service/vector_store.py

from chromadb import Client
from chromadb.config import Settings

class VectorStore:
    def __init__(self):
        self.client = Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        self.collection = self.client.get_or_create_collection(
            name="portfolio_docs",
            metadata={"description": "Vasu's portfolio documentation"}
        )

    def add_documents(self, documents, embeddings, metadatas):
        """Add documents to vector store"""
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=[f"doc_{i}" for i in range(len(documents))]
        )

    def search(self, query_embedding, k=5):
        """Search for similar documents"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results
```

### Document Ingestion

```python
# backend/rag_service/ingest.py

import os
from pathlib import Path
from openai import OpenAI

class DocumentIngestion:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.client = OpenAI()

    def ingest_markdown_files(self, directory):
        """Ingest all markdown files from directory"""
        docs_path = Path(directory)

        for md_file in docs_path.rglob("*.md"):
            with open(md_file, 'r') as f:
                content = f.read()

            # Chunk the document
            chunks = self.chunk_text(content)

            # Generate embeddings
            embeddings = self.generate_embeddings(chunks)

            # Store in vector database
            metadatas = [{
                "source": str(md_file),
                "chunk_id": i,
                "total_chunks": len(chunks)
            } for i in range(len(chunks))]

            self.vector_store.add_documents(
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas
            )

    def chunk_text(self, text, chunk_size=500, overlap=50):
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)

        return chunks

    def generate_embeddings(self, texts):
        """Generate embeddings using OpenAI"""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        return [item.embedding for item in response.data]
```

### RAG Query Implementation

```python
# backend/rag_service/chatbot.py

from openai import OpenAI

class RAGChatbot:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.client = OpenAI()

    def query(self, question: str):
        """Answer question using RAG"""
        # Generate query embedding
        query_embedding = self.generate_embedding(question)

        # Search vector store
        results = self.vector_store.search(query_embedding, k=5)

        # Build context from results
        context = "\n\n".join(results['documents'][0])

        # Generate answer
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are an AI assistant helping visitors
                    learn about Vasu Kapoor's journey to becoming an AI/ML
                    Platform Engineer. Answer based ONLY on the provided
                    context. Be specific, cite sources, and include relevant
                    links. If you don't know, say so."""
                },
                {
                    "role": "user",
                    "content": f"""Context: {context}

                    Question: {question}

                    Answer:"""
                }
            ]
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": results['metadatas'][0],
            "context_used": len(results['documents'][0])
        }

    def generate_embedding(self, text):
        """Generate embedding for text"""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
```

### Frontend Chatbot Widget

```jsx
// frontend/src/components/chatbot/ChatWidget.jsx

import { useState } from 'react';
import axios from 'axios';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hi! I'm Vasu's AI assistant. Ask me anything about his journey to AI/ML Platform Engineering!"
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post('/api/chatbot/query/', {
        question: input
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.answer,
        sources: response.data.sources
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chatbot error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-600 text-white rounded-full p-4 shadow-lg hover:bg-blue-700"
        >
          💬 Ask Me Anything
        </button>
      )}

      {isOpen && (
        <div className="bg-white rounded-lg shadow-2xl w-96 h-[500px] flex flex-col">
          <div className="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
            <h3 className="font-bold">Vasu's AI Assistant</h3>
            <button onClick={() => setIsOpen(false)}>✕</button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={msg.role === 'user' ? 'text-right' : 'text-left'}
              >
                <div
                  className={`inline-block p-3 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  {msg.content}
                </div>
                {msg.sources && (
                  <div className="text-xs text-gray-500 mt-1">
                    Sources: {msg.sources.length} documents
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="text-left">
                <div className="inline-block p-3 rounded-lg bg-gray-100">
                  Thinking...
                </div>
              </div>
            )}
          </div>

          <div className="p-4 border-t">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Ask about Vasu's journey..."
                className="flex-1 border rounded-lg px-3 py-2"
              />
              <button
                onClick={sendMessage}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```
