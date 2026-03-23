"""
Security detector module for the Agentic AI Security System.
Handles classification of user inputs for security threats using LangChain.
"""

from llm.model import LLMModel
from utils.prompts import get_security_classification_prompt

class SecurityDetector:
    def __init__(self, llm_model: LLMModel):
        """
        Initialize the security detector with an LLM model.

        Args:
            llm_model (LLMModel): The LLM model instance to use for classification.
        """
        self.llm_model = llm_model

    def is_safe(self, user_input: str) -> bool:
        """
        Determine if the user input is safe based on LLM classification.

        Args:
            user_input (str): The user's input text to check.

        Returns:
            bool: True if safe, False if contains security threats.
        """
        prompt = get_security_classification_prompt(user_input)
        classification = self.llm_model.classify_input(prompt)

        # Parse the response: "safe" or "unsafe: category"
        classification = classification.strip().lower()

        if classification == "safe" or classification.startswith("safe"):
            return True

        if classification.startswith("unsafe:"):
            unsafe_category = classification.split(":", 1)[1].strip() if ":" in classification else ""
            # Only block known threat categories
            if unsafe_category in [
                "prompt injection",
                "indirect prompt injection",
                "data leakage",
                "data poisoning"
            ]:
                return False

        # If classification is unclear or unknown, treat as safe
        return True

    def get_classification(self, user_input: str) -> str:
        """
        Get the security classification for the user input.

        Args:
            user_input (str): The user's input text.

        Returns:
            str: The classification response (safe or unsafe: category).
        """
        prompt = get_security_classification_prompt(user_input)
        classification = self.llm_model.classify_input(prompt).strip().lower()

        # Known categories
        known_categories = [
            "prompt injection",
            "indirect prompt injection",
            "data leakage",
            "data poisoning"
        ]

        if classification == "safe":
            return "safe"

        if classification.startswith("unsafe:"):
            unsafe_category = classification.split(":", 1)[1].strip()
            if unsafe_category in known_categories:
                return f"unsafe: {unsafe_category}"

        # fallback to safe for unknown classification outputs
        return "safe"