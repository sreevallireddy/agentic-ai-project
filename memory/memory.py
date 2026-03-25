"""
Conversation memory management for the Agentic AI System.
Stores and manages conversation history.
"""

from typing import List, Dict
from collections import deque


class ConversationMemory:
    """
    Manages conversation history with a fixed size.
    """

    def __init__(self, max_history: int = 5):
        """
        Initialize conversation memory.

        Args:
            max_history (int): Maximum number of past interactions to keep.
        """
        self.max_history = max_history
        self.history = deque(maxlen=max_history)

    def add_interaction(self, user_input: str, assistant_response: str):
        """
        Add a user-assistant interaction to history.

        Args:
            user_input (str): User's input message.
            assistant_response (str): Assistant's response.
        """
        self.history.append({
            "user": user_input,
            "assistant": assistant_response
        })

    def get_history_string(self) -> str:
        """
        Get conversation history as a formatted string.

        Returns:
            str: Formatted conversation history.
        """
        if not self.history:
            return "No previous conversation."

        history_str = "Previous conversation:\n"
        for i, interaction in enumerate(self.history):
            history_str += f"\nUser {i+1}: {interaction['user']}\n"
            history_str += f"Assistant {i+1}: {interaction['assistant']}\n"

        return history_str

    def get_context(self) -> str:
        """Get memory context for LLM prompt."""
        return self.get_history_string()

    def clear(self):
        """Clear conversation history."""
        self.history.clear()

    def __len__(self):
        """Get number of interactions in history."""
        return len(self.history)
