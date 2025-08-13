"""
llm_integration.py - Intégration LLM pour le Chatbot ODD

Ce module gère l'intégration avec un modèle LLM local (google/flan-t5-small) pour générer des réponses naturelles à partir des questions utilisateur.
"""

from transformers import pipeline
from typing import Optional, Any

class LLMIntegration:
    """
    Classe d'intégration pour le modèle LLM local (Flan-T5 Small).
    Permet de générer des réponses textuelles à partir de questions utilisateur.
    """
    def __init__(self) -> None:
        """
        Initialise le pipeline de génération textuelle avec un modèle léger.
        """
        self.generator = pipeline("text2text-generation", model="google/flan-t5-small")

    def generate_response(self, question: str, odd_data: Optional[Any] = None) -> str:
        """
        Génère une réponse à partir d'une question en utilisant le pipeline LLM local.
        Args:
            question (str): La question utilisateur.
            odd_data (Any, optionnel): Données ODD additionnelles pour le contexte (non utilisé ici).
        Returns:
            str: Réponse générée ou message d'erreur.
        """
        response = self.generator(question, max_new_tokens=64, do_sample=True, temperature=0.7)
        return response[0].get('generated_text', str(response[0]))

llm_integration = LLMIntegration()