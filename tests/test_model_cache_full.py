import pytest
from model_cache import ModelCache
import os
import tempfile

def test_model_cache_init():
    cache = ModelCache()
    assert os.path.exists(cache.cache_dir)

def test_get_cache_path():
    cache = ModelCache()
    path = cache._get_cache_path('testfile.txt')
    assert path.endswith('testfile.txt')

def test_get_data_hash():
    cache = ModelCache()
    h = cache._get_data_hash({'a': 1})
    assert isinstance(h, str)

def test_clear_cache():
    cache = ModelCache()
    # Create a dummy file
    dummy = os.path.join(cache.cache_dir, 'dummy.txt')
    with open(dummy, 'w') as f:
        f.write('x')
    assert os.path.exists(dummy)
    cache.clear_cache()
    assert not os.path.exists(dummy)

def test_get_cache_info():
    cache = ModelCache()
    info = cache.get_cache_info()
    assert isinstance(info, dict)
