"""
Document loader for RAG pipeline.
Loads text and PDF documents for vector embedding.
"""

import os
from typing import List


class DocumentLoader:
    """Load documents from files."""

    @staticmethod
    def load_documents(directory: str = "./docs") -> List[dict]:
        """
        Load all .txt and .pdf files from a directory.

        Args:
            directory (str): Path to directory containing documents.

        Returns:
            List[dict]: List of documents with 'filename' and 'content' keys.
        """
        documents = []

        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist. Returning empty list.")
            return documents

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if filename.endswith(".txt"):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append({
                            "filename": filename,
                            "content": content
                        })
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")

            elif filename.endswith(".pdf"):
                try:
                    # Placeholder for PDF loading
                    # In production, use PyPDF2 or similar
                    print(f"PDF support: Install PyPDF2 for {filename}")
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")

        return documents


def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks with overlap.

    Args:
        text (str): Text to split.
        chunk_size (int): Size of each chunk.
        overlap (int): Overlap between chunks.

    Returns:
        List[str]: List of text chunks.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks
