
"""
llm_integration.py - LLM Integration for the SDG Chatbot

This module manages integration with a local LLM model (google/flan-t5-small) to generate natural responses from user questions.
"""



# All imports at the very top
from transformers import pipeline
from typing import Optional, Any

"""
llm_integration.py - LLM Integration for the SDG Chatbot

This module manages integration with a local LLM model (google/flan-t5-small) to generate natural responses from user questions.
"""

class LLMIntegration:
    """
    Integration class for the local LLM model (Flan-T5 Small).
    Allows generating textual responses from user questions.
    """
    def __init__(self) -> None:
        """
        Initialize the text generation pipeline with a lightweight model.
        """
        self.generator = pipeline("text2text-generation", model="google/flan-t5-small")

    def generate_response(self, question: str, odd_data: Optional[Any] = None) -> str:
        """
        Generate a response from a question using the local LLM pipeline.
        Args:
            question (str): The user's question.
            odd_data (Any, optional): Additional SDG data for context (not used here).
        Returns:
            str: Generated response or error message.
        """
        response = self.generator(question, max_new_tokens=64, do_sample=True, temperature=0.7)
        return response[0].get('generated_text', str(response[0]))

llm_integration = LLMIntegration()