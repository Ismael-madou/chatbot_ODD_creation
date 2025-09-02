import pytest
from llm_integration import LLMIntegration

def test_llm_integration_init():
    # Should not raise
    try:
        llm = LLMIntegration()
    except Exception as e:
        pytest.fail(f"LLMIntegration init raised: {e}")

def test_generate_response():
    llm = LLMIntegration()
    result = llm.generate_response("What is SDG 1?")
    assert isinstance(result, str)
