import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main

def test_run_demo():
    # Should not raise
    try:
        main.run_demo()
    except Exception as e:
        pytest.fail(f"run_demo raised: {e}")
