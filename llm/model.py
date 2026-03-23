"""
LLM model utilities for the Agentic AI Security System.
Uses LangChain with Hugging Face transformers.
"""

import torch
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

class LLMModel:
    def __init__(self):
        """
        Initialize the LLM model using LangChain and Hugging Face.
        Loads the google/flan-t5-base model.
        """
        print("Loading LLM model... This may take a moment.")
        
        # Determine device
        if torch.cuda.is_available():
            device = 0  # Use first GPU
        elif torch.backends.mps.is_available():
            device = -1  # Use CPU (MPS has issues with meta tensors)
        else:
            device = -1  # Use CPU
        
        # Create the transformers pipeline
        hf_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device=device,
            max_length=200,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            model_kwargs={"load_in_8bit": False}
        )
        # Wrap with LangChain
        self.llm = HuggingFacePipeline(pipeline=hf_pipeline)
        print("Model loaded successfully.")

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response using the LLM based on the given prompt.

        Args:
            prompt (str): The input prompt for generation.

        Returns:
            str: The generated response text.
        """
        try:
            response = self.llm.invoke(prompt)
            return response.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def classify_input(self, prompt: str) -> str:
        """
        Classify user input for security threats using the LLM.

        Args:
            prompt (str): The classification prompt.

        Returns:
            str: The classification response (safe or unsafe: category).
        """
        try:
            response = self.llm.invoke(prompt)
            return response.strip().lower()
        except Exception as e:
            print(f"Error in classification: {str(e)}")
            return "safe"  # Default to safe on error