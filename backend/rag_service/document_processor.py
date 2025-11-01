"""
Document processing and ingestion
Loads markdown files and prepares them for vector storage
"""
import os
from pathlib import Path
import re

class DocumentProcessor:
    """Process and chunk documents for RAG system"""

    def __init__(self, chunk_size=500, overlap=50):
        """
        Initialize document processor

        Args:
            chunk_size: Number of words per chunk
            overlap: Number of words to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def load_markdown_files(self, directory):
        """
        Load all markdown files from a directory

        Args:
            directory: Path to directory containing markdown files

        Returns:
            List of (content, metadata) tuples
        """
        docs_path = Path(directory)
        documents = []

        for md_file in docs_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract metadata
                metadata = {
                    'source': str(md_file.relative_to(docs_path.parent)),
                    'filename': md_file.name,
                    'category': self._infer_category(md_file)
                }

                documents.append((content, metadata))
                print(f"  📄 Loaded: {md_file.name}")

            except Exception as e:
                print(f"  ⚠️  Error loading {md_file}: {e}")

        print(f"✅ Loaded {len(documents)} markdown files")
        return documents

    def _infer_category(self, filepath):
        """Infer category from file path"""
        path_str = str(filepath)

        if 'journey' in path_str:
            return 'journey'
        elif 'technical' in path_str or 'architecture' in path_str:
            return 'technical'
        elif 'planning' in path_str:
            return 'planning'
        elif 'blog' in path_str:
            return 'blog'
        else:
            return 'general'

    def chunk_text(self, text):
        """
        Split text into overlapping chunks

        Args:
            text: Input text string

        Returns:
            List of text chunks
        """
        # Clean the text
        text = self._clean_text(text)

        # Split into words
        words = text.split()

        if len(words) <= self.chunk_size:
            return [text]

        chunks = []
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk = " ".join(words[i:i + self.chunk_size])
            if chunk.strip():  # Only add non-empty chunks
                chunks.append(chunk)

        return chunks

    def _clean_text(self, text):
        """Clean and normalize text"""
        # Remove multiple newlines
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Remove markdown image syntax
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def process_documents(self, documents):
        """
        Process documents into chunks with metadata

        Args:
            documents: List of (content, metadata) tuples

        Returns:
            Tuple of (chunks, metadatas)
        """
        all_chunks = []
        all_metadatas = []

        for content, base_metadata in documents:
            chunks = self.chunk_text(content)

            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)

                # Create metadata for each chunk
                chunk_metadata = base_metadata.copy()
                chunk_metadata.update({
                    'chunk_id': i,
                    'total_chunks': len(chunks),
                    'chunk_size': len(chunk.split())
                })

                all_metadatas.append(chunk_metadata)

        print(f"✅ Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks, all_metadatas
