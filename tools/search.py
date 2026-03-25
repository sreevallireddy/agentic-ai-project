"""
Search tool for the Agentic AI System.
Simulates or integrates with a search API.
"""

import json
from typing import List, Dict


class SearchTool:
    """
    Search tool for querying information.
    """

    # Mock search results database
    MOCK_RESULTS = {
        "artificial intelligence": [
            "AI is the simulation of human intelligence processes.",
            "Machine learning is a subset of artificial intelligence.",
            "Deep learning uses neural networks with multiple layers."
        ],
        "python programming": [
            "Python is a high-level programming language.",
            "Python is known for its simple and readable syntax.",
            "Python has many libraries like NumPy, Pandas, and TensorFlow."
        ],
        "web development": [
            "Web development involves building websites and web applications.",
            "Frontend frameworks include React, Vue, and Angular.",
            "Backend frameworks include Django, Flask, and FastAPI."
        ]
    }

    @staticmethod
    def search(query: str, num_results: int = 3) -> List[str]:
        """
        Search for information related to the query.

        Args:
            query (str): Search query.
            num_results (int): Number of results to return.

        Returns:
            List[str]: List of search results.
        """
        query_lower = query.lower()

        # Check for matching keywords in mock results
        for keyword, results in SearchTool.MOCK_RESULTS.items():
            if keyword in query_lower:
                return results[:num_results]

        # Default: return generic results
        return [
            f"Information about '{query}'",
            f"Results for search query: '{query}'",
            f"Related content for: '{query}'"
        ]

    @staticmethod
    def is_search_needed(user_input: str) -> bool:
        """Check if search tool is needed."""
        search_keywords = ["search", "find", "look up", "what is", "tell me about", "information"]
        return any(keyword in user_input.lower() for keyword in search_keywords)
