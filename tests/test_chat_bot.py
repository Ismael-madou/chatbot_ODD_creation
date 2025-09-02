import pytest
from src.chat_bot import chercher_odd

def test_chercher_odd_basic():
    question = "Qu'est-ce que l'ODD 1 ?"
    result = chercher_odd(question, lang="Français")
    assert isinstance(result, dict) or isinstance(result, str)
    assert result
