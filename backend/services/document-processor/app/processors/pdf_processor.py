# PDF Processing Module
import io
import logging
from typing import List, Dict, Any
import httpx
from PyPDF2 import PdfReader
import pdfplumber

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Process PDF documents and extract text"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    async def download_pdf(self, url: str) -> bytes:
        """Download PDF from URL"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content
        except Exception as e:
            logger.error(f"Failed to download PDF from {url}: {e}")
            raise

    def extract_text_pypdf2(self, pdf_bytes: bytes) -> str:
        """Extract text using PyPDF2"""
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_file)

            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
            raise

    def extract_text_pdfplumber(self, pdf_bytes: bytes) -> str:
        """Extract text using pdfplumber (fallback)"""
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            text_parts = []

            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)

            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {e}")
            raise

    def extract_text(self, pdf_bytes: bytes) -> str:
        """Extract text from PDF (try PyPDF2, fallback to pdfplumber)"""
        try:
            # Try PyPDF2 first
            text = self.extract_text_pypdf2(pdf_bytes)
            if text and len(text.strip()) > 100:
                logger.info("Successfully extracted text with PyPDF2")
                return text
        except Exception as e:
            logger.warning(f"PyPDF2 failed, trying pdfplumber: {e}")

        try:
            # Fallback to pdfplumber
            text = self.extract_text_pdfplumber(pdf_bytes)
            if text and len(text.strip()) > 0:
                logger.info("Successfully extracted text with pdfplumber")
                return text
        except Exception as e:
            logger.error(f"Both extraction methods failed: {e}")
            raise Exception("Failed to extract text from PDF")

        raise Exception("No text extracted from PDF")

    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Split text into chunks with overlap"""
        if not text:
            return []

        chunks = []
        text_length = len(text)
        start = 0

        chunk_index = 0
        while start < text_length:
            end = start + self.chunk_size

            # Try to break at sentence or paragraph boundary
            if end < text_length:
                # Look for paragraph break
                next_break = text.find("\n\n", end - 100, end + 100)
                if next_break != -1:
                    end = next_break
                else:
                    # Look for sentence break
                    for punct in [". ", "! ", "? "]:
                        next_break = text.find(punct, end - 100, end + 100)
                        if next_break != -1:
                            end = next_break + len(punct)
                            break

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk_metadata = {
                    "chunk_index": chunk_index,
                    "start_char": start,
                    "end_char": end,
                    "chunk_size": len(chunk_text),
                }

                if metadata:
                    chunk_metadata.update(metadata)

                chunks.append({
                    "text": chunk_text,
                    "metadata": chunk_metadata,
                })

                chunk_index += 1

            # Move start position with overlap
            start = end - self.chunk_overlap if end < text_length else text_length

        logger.info(f"Created {len(chunks)} chunks from text ({text_length} chars)")
        return chunks

    async def process_pdf(self, url: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Download PDF, extract text, and chunk it"""
        # Download PDF
        pdf_bytes = await self.download_pdf(url)
        logger.info(f"Downloaded PDF: {len(pdf_bytes)} bytes")

        # Extract text
        text = self.extract_text(pdf_bytes)
        logger.info(f"Extracted text: {len(text)} characters")

        # Chunk text
        chunks = self.chunk_text(text, metadata)

        return chunks
