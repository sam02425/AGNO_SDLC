"""
Knowledge base loaders for the SDLC workflow.
"""
import os
import faiss
import numpy as np
from typing import List, Dict, Any, Optional
from agno.embedder.openai import OpenAIEmbedder

class FAISSKnowledgeBase:
    """
    Knowledge base using FAISS for vector storage and retrieval.
    """
    def __init__(self,
                 docs_path: str,
                 index_path: Optional[str] = None,
                 embedder = None):
        """
        Initialize the FAISS knowledge base.

        Args:
            docs_path: Path to the documents directory
            index_path: Path to save the FAISS index (defaults to docs_path/index.faiss)
            embedder: Embedder to use for document embedding
        """
        self.docs_path = docs_path
        self.index_path = index_path or os.path.join(docs_path, "index.faiss")
        self.embedder = embedder or OpenAIEmbedder(id="text-embedding-3-small")

        self.documents = []
        self.index = None

        # Create documents directory if it doesn't exist
        os.makedirs(docs_path, exist_ok=True)

    def load_documents(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Load documents from file paths.

        Args:
            file_paths: List of file paths to load

        Returns:
            List of loaded documents
        """
        documents = []

        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split content into chunks
            chunks = self._split_into_chunks(content, chunk_size=512)

            for i, chunk in enumerate(chunks):
                documents.append({
                    'id': f"{os.path.basename(file_path)}-{i}",
                    'source': file_path,
                    'content': chunk
                })

        self.documents = documents
        return documents

    def _split_into_chunks(self, text: str, chunk_size: int = 512) -> List[str]:
        """Split text into chunks of approximately chunk_size characters."""
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        current_chunk = ""

        for paragraph in text.split('\n\n'):
            if len(current_chunk) + len(paragraph) <= chunk_size:
                current_chunk += paragraph + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + '\n\n'

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def build_index(self) -> None:
        """Build the FAISS index from the loaded documents."""
        if not self.documents:
            raise ValueError("No documents loaded. Call load_documents first.")

        # Get embeddings for all documents
        texts = [doc['content'] for doc in self.documents]
        embeddings = self.embedder.embed_documents(texts)

        # Convert to numpy array
        embeddings_np = np.array(embeddings).astype('float32')

        # Create FAISS index
        dimension = embeddings_np.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings_np)

        # Save index
        faiss.write_index(self.index, self.index_path)

    def load_index(self) -> None:
        """Load the FAISS index from disk."""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:
            raise FileNotFoundError(f"Index file not found at {self.index_path}")

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search the knowledge base for documents matching the query.

        Args:
            query: Query text
            k: Number of results to return

        Returns:
            List of matching documents with scores
        """
        if self.index is None:
            raise ValueError("Index not built or loaded. Call build_index or load_index first.")

        # Get query embedding
        query_embedding = self.embedder.embed_query(query)
        query_np = np.array([query_embedding]).astype('float32')

        # Search index
        distances, indices = self.index.search(query_np, k)

        # Get matching documents
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                results.append({
                    **self.documents[idx],
                    'score': float(distances[0][i])
                })

        return results