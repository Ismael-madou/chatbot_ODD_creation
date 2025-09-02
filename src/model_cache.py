
"""
model_cache.py - Cache management for models, embeddings, and stores of the SDG Chatbot

This module manages saving, loading, and cache handling for SentenceTransformer models, Haystack document stores, embeddings, and BM25 retrievers.
"""

"""
model_cache.py - Cache management for models, embeddings, and stores of the SDG Chatbot

This module manages saving, loading, and cache handling for SentenceTransformer models, Haystack document stores, embeddings, and BM25 retrievers.
"""

# All imports at the very top
from sentence_transformers import SentenceTransformer
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
import pickle
import os
import json
from typing import Dict, Any, Optional
import hashlib

class ModelCache:
    """
    Utility class for managing cache of models, embeddings, document stores, and retrievers.
    Allows fast saving and reloading of heavy objects to speed up chatbot startup.
    """
    def __init__(self, cache_dir: str = None) -> None:
        """
        Initialize the cache directory.
        Args:
            cache_dir (str): Directory to store cache files.
        """
        if cache_dir is None:
            # Place cache at the project root
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            cache_dir = os.path.join(project_root, 'cache')
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, filename: str) -> str:
        """
        Return the absolute path of a cache file.
        Args:
            filename (str): File name.
        Returns:
            str: Full path.
        """
        return os.path.join(self.cache_dir, filename)

    def _get_data_hash(self, data: Dict) -> str:
        """
        Compute an MD5 hash from a data dictionary (for cache versioning).
        Args:
            data (Dict): Data to hash.
        Returns:
            str: MD5 hash.
        """
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()

    def save_model(self, model: SentenceTransformer, model_name: str = "sentence_transformer") -> None:
        """
        Save a SentenceTransformer model to the cache.
        Args:
            model (SentenceTransformer): The model to save.
            model_name (str): Cache file name.
        """
        cache_path = self._get_cache_path(f"{model_name}.pkl")
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(model, f)
            print(f"✅ Model saved: {cache_path}")
        except Exception as e:
            print(f"❌ Model save error: {e}")

    def load_model(self, model_name: str = "sentence_transformer") -> Optional[SentenceTransformer]:
        """
        Load a SentenceTransformer model from the cache.
        Args:
            model_name (str): Cache file name.
        Returns:
            Optional[SentenceTransformer]: Loaded model or None.
        """
        cache_path = self._get_cache_path(f"{model_name}.pkl")
        try:
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    model = pickle.load(f)
                print(f"✅ Model loaded from cache: {cache_path}")
                return model
            else:
                print("⚠️  Model cache not found, loading from HuggingFace...")
                return None
        except Exception as e:
            print(f"❌ Model load error: {e}")
            return None

    def save_document_store(self, document_store: InMemoryDocumentStore, data_hash: str) -> None:
        """
        Save a Haystack document store to the cache.
        Args:
            document_store (InMemoryDocumentStore): Document store to save.
            data_hash (str): Data hash for cache versioning.
        """
        cache_path = self._get_cache_path(f"document_store_{data_hash}.pkl")
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(document_store, f)
            print(f"✅ Document store saved: {cache_path}")
        except Exception as e:
            print(f"❌ Document store save error: {e}")

    def load_document_store(self, data_hash: str) -> Optional[InMemoryDocumentStore]:
        """
        Load a Haystack document store from the cache.
        Args:
            data_hash (str): Data hash for cache versioning.
        Returns:
            Optional[InMemoryDocumentStore]: Loaded document store or None.
        """
        cache_path = self._get_cache_path(f"document_store_{data_hash}.pkl")
        try:
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    document_store = pickle.load(f)
                print(f"✅ Document store loaded from cache: {cache_path}")
                return document_store
            else:
                print("⚠️  Document store cache not found")
                return None
        except Exception as e:
            print(f"❌ Document store load error: {e}")
            return None

    def save_embeddings(self, embeddings: Dict[str, Any], data_hash: str) -> None:
        """
        Save embeddings to the cache.
        Args:
            embeddings (Dict[str, Any]): Embeddings to save.
            data_hash (str): Data hash for cache versioning.
        """
        cache_path = self._get_cache_path(f"embeddings_{data_hash}.pkl")
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(embeddings, f)
            print(f"✅ Embeddings saved: {cache_path}")
        except Exception as e:
            print(f"❌ Embeddings save error: {e}")

    def load_embeddings(self, data_hash: str) -> Optional[Dict[str, Any]]:
        """
        Load embeddings from the cache.
        Args:
            data_hash (str): Data hash for cache versioning.
        Returns:
            Optional[Dict[str, Any]]: Loaded embeddings or None.
        """
        cache_path = self._get_cache_path(f"embeddings_{data_hash}.pkl")
        try:
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    embeddings = pickle.load(f)
                print(f"✅ Embeddings loaded from cache: {cache_path}")
                return embeddings
            else:
                print("⚠️  Embeddings cache not found")
                return None
        except Exception as e:
            print(f"❌ Embeddings load error: {e}")
            return None

    def save_retriever(self, retriever: BM25Retriever, data_hash: str) -> None:
        """
        Save a BM25 retriever to the cache.
        Args:
            retriever (BM25Retriever): Retriever to save.
            data_hash (str): Data hash for cache versioning.
        """
        cache_path = self._get_cache_path(f"retriever_{data_hash}.pkl")
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(retriever, f)
            print(f"✅ Retriever saved: {cache_path}")
        except Exception as e:
            print(f"❌ Retriever save error: {e}")

    def load_retriever(self, data_hash: str) -> Optional[BM25Retriever]:
        """
        Load a BM25 retriever from the cache.
        Args:
            data_hash (str): Data hash for cache versioning.
        Returns:
            Optional[BM25Retriever]: Loaded retriever or None.
        """
        cache_path = self._get_cache_path(f"retriever_{data_hash}.pkl")
        try:
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    retriever = pickle.load(f)
                print(f"✅ Retriever loaded from cache: {cache_path}")
                return retriever
            else:
                print("⚠️  Retriever cache not found")
                return None
        except Exception as e:
            print(f"❌ Retriever load error: {e}")
            return None

    def clear_cache(self) -> None:
        """
        Delete all files in the cache.
        """
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("✅ Cache cleared")
        except Exception as e:
            print(f"❌ Cache clear error: {e}")

    def get_cache_info(self) -> Dict[str, Any]:
        """
        Return information about the cache (number of files, total size, etc.).
        Returns:
            Dict[str, Any]: Cache info.
        """
        cache_info = {
            "cache_dir": self.cache_dir,
            "files": [],
            "total_size": 0
        }
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    cache_info["files"].append({
                        "name": filename,
                        "size": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2)
                    })
                    cache_info["total_size"] += file_size
            cache_info["total_size_mb"] = round(cache_info["total_size"] / (1024 * 1024), 2)
            cache_info["file_count"] = len(cache_info["files"])
        except Exception as e:
            print(f"❌ Cache info read error: {e}")
        return cache_info

# Global instance
model_cache = ModelCache()