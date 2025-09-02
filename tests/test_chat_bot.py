import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from chat_bot import chercher_odd

def test_chercher_odd_basic():
    # Test a basic SDG question in French
    question = "Qu'est-ce que l'ODD 1 ?"
    result = chercher_odd(question, lang="Français")
    assert isinstance(result, dict) or isinstance(result, str)
    assert result
