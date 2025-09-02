import os
import pytest
from src.model_cache import ModelCache

def test_cache_creation_and_clear():
    cache_dir = os.path.join(os.path.dirname(__file__), 'test_cache')
    cache = ModelCache(cache_dir)
    # Création d'un fichier fictif
    test_file = os.path.join(cache_dir, 'dummy.txt')
    with open(test_file, 'w') as f:
        f.write('test')
    assert os.path.exists(test_file)
    cache.clear_cache()
    assert not os.path.exists(test_file)
    os.rmdir(cache_dir)
