"""
FAISS-based vector store for document retrieval and similarity search.
"""

import os
import pickle
from typing import List, Tuple
import json


class FAISSVectorStore:
    """
    Vector store using FAISS for efficient similarity search.
    """

    def __init__(self, embeddings_model=None):
        """
        Initialize the vector store.

        Args:
            embeddings_model: HuggingFaceEmbeddings instance for creating embeddings.
        """
        self.embeddings_model = embeddings_model
        self.index = None
        self.documents = []
        self.embeddings = []

    def add_documents(self, documents: List[dict], metadata: List[dict] = None):
        """
        Add documents to the vector store.

        Args:
            documents (List[dict]): List of documents with 'content' key.
            metadata (List[dict]): Optional metadata for each document.
        """
        if self.embeddings_model is None:
            print("Warning: No embeddings model provided. Using mock embeddings.")
            self._add_mock_documents(documents, metadata)
            return

        try:
            import faiss
            import numpy as np
        except ImportError:
            print("FAISS not installed. Using mock vector store.")
            self._add_mock_documents(documents, metadata)
            return

        for i, doc in enumerate(documents):
            content = doc.get("content", "")
            embedding = self.embeddings_model.embed_query(content)
            self.documents.append({
                "content": content,
                "metadata": metadata[i] if metadata else {}
            })
            self.embeddings.append(embedding)

        # Create FAISS index
        if self.embeddings:
            embeddings_array = np.array(self.embeddings).astype('float32')
            self.index = faiss.IndexFlatL2(embeddings_array.shape[1])
            self.index.add(embeddings_array)

    def _add_mock_documents(self, documents: List[dict], metadata: List[dict] = None):
        """Mock implementation for testing without embeddings."""
        for i, doc in enumerate(documents):
            self.documents.append({
                "content": doc.get("content", ""),
                "metadata": metadata[i] if metadata else {}
            })

    def similarity_search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        """
        Search for similar documents.

        Args:
            query (str): Search query.
            k (int): Number of results to return.

        Returns:
            List[Tuple[str, float]]: List of (document_content, score) tuples.
        """
        if not self.documents:
            return []

        if self.index is None:
            # Mock search: return first k documents
            return [(doc["content"], 1.0 - (i * 0.1)) for i, doc in enumerate(self.documents[:k])]

        try:
            query_embedding = self.embeddings_model.embed_query(query)
            import numpy as np
            query_array = np.array([query_embedding]).astype('float32')
            distances, indices = self.index.search(query_array, k)

            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(self.documents):
                    score = 1.0 / (1.0 + distance)  # Convert distance to similarity
                    results.append((self.documents[idx]["content"], score))
            return results
        except Exception as e:
            print(f"Error in similarity search: {str(e)}")
            return [(doc["content"], 1.0) for doc in self.documents[:k]]

    def save(self, path: str):
        """Save vector store to disk."""
        os.makedirs(path, exist_ok=True)
        # Save documents and metadata
        with open(os.path.join(path, "documents.json"), 'w') as f:
            json.dump(self.documents, f)
        # Note: FAISS index saving requires numpy/faiss

    def load(self, path: str):
        """Load vector store from disk."""
        try:
            with open(os.path.join(path, "documents.json"), 'r') as f:
                self.documents = json.load(f)
        except FileNotFoundError:
            print(f"Vector store not found at {path}")
