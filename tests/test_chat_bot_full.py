import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import chat_bot

def test_get_llm_pipeline():
    # Should return a pipeline or None
    result = chat_bot.get_llm_pipeline()
    assert result is None or hasattr(result, '__call__')

def test_generer_reponse_llm():
    # Should return a string (error or answer)
    result = chat_bot.generer_reponse_llm("What is SDG 1?")
    assert isinstance(result, str)

def test_initialize_chatbot():
    # Should not raise
    try:
        chat_bot.initialize_chatbot()
    except Exception as e:
        pytest.fail(f"initialize_chatbot raised: {e}")

def test_create_haystack_store():
    # Should return None or a document store
    result = chat_bot.create_haystack_store()
    assert result is None or hasattr(result, 'write_documents')

def test_chercher_odd():
    # Should return a dict or error
    result = chat_bot.chercher_odd("What is SDG 1?", lang="English")
    assert isinstance(result, dict)

def test_formater_reponse_odd():
    # Should return a string
    odd_data = {"odd": 1, "title": {"en": "No Poverty"}, "description": {"en": "End poverty in all its forms everywhere."}}
    result = chat_bot.formater_reponse_odd(odd_data, question="What is SDG 1?", lang="English")
    assert isinstance(result, str)

def test_clear_cache():
    # Should not raise
    try:
        chat_bot.clear_cache()
    except Exception as e:
        pytest.fail(f"clear_cache raised: {e}")

def test_get_cache_info():
    # Should return a dict
    result = chat_bot.get_cache_info()
    assert isinstance(result, dict)
