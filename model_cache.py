"""
model_cache.py - Gestion du cache pour les modèles, embeddings et stores du Chatbot ODD

Ce module gère la sauvegarde, le chargement et la gestion du cache pour les modèles SentenceTransformer, les document stores Haystack, les embeddings et les retrievers BM25.
"""

import pickle
import os
import json
from sentence_transformers import SentenceTransformer
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
from typing import Dict, Any, Optional
import hashlib

class ModelCache:
    """
    Classe utilitaire pour la gestion du cache des modèles, embeddings, document stores et retrievers.
    Permet de sauvegarder et recharger rapidement les objets lourds pour accélérer le démarrage du chatbot.
    """
    def __init__(self, cache_dir: str = "cache") -> None:
        """
        Initialise le répertoire de cache.
        Args:
            cache_dir (str): Dossier où stocker les fichiers de cache.
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, filename: str) -> str:
        """
        Retourne le chemin absolu d'un fichier de cache.
        Args:
            filename (str): Nom du fichier.
        Returns:
            str: Chemin complet.
        """
        return os.path.join(self.cache_dir, filename)

    def _get_data_hash(self, data: Dict) -> str:
        """
        Calcule un hash MD5 à partir d'un dictionnaire de données (pour versionner le cache).
        Args:
            data (Dict): Données à hasher.
        Returns:
            str: Hash MD5.
        """
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()

    def save_model(self, model: SentenceTransformer, model_name: str = "sentence_transformer") -> None:
        """
        Sauvegarde un modèle SentenceTransformer dans le cache.
        Args:
            model (SentenceTransformer): Le modèle à sauvegarder.
            model_name (str): Nom du fichier de cache.
        """
        cache_path = self._get_cache_path(f"{model_name}.pkl")
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(model, f)
            print(f"✅ Modèle sauvegardé: {cache_path}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde modèle: {e}")

    def load_model(self, model_name: str = "sentence_transformer") -> Optional[SentenceTransformer]:
        """
        Charge un modèle SentenceTransformer depuis le cache.
        Args:
            model_name (str): Nom du fichier de cache.
        Returns:
            Optional[SentenceTransformer]: Le modèle chargé ou None.
        """
        cache_path = self._get_cache_path(f"{model_name}.pkl")
        try:
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    model = pickle.load(f)
                print(f"✅ Modèle chargé depuis le cache: {cache_path}")
                return model
            else:
                print("⚠️  Cache modèle non trouvé, chargement depuis HuggingFace...")
                return None
        except Exception as e:
            print(f"❌ Erreur chargement modèle: {e}")
            return None

    def save_document_store(self, document_store: InMemoryDocumentStore, data_hash: str) -> None:
        """
        Sauvegarde un document store Haystack dans le cache.
        Args:
            document_store (InMemoryDocumentStore): Le document store à sauvegarder.
            data_hash (str): Hash des données pour versionner le cache.
        """
        cache_path = self._get_cache_path(f"document_store_{data_hash}.pkl")
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(document_store, f)
            print(f"✅ Document store sauvegardé: {cache_path}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde document store: {e}")

    def load_document_store(self, data_hash: str) -> Optional[InMemoryDocumentStore]:
        """
        Charge un document store Haystack depuis le cache.
        Args:
            data_hash (str): Hash des données pour versionner le cache.
        Returns:
            Optional[InMemoryDocumentStore]: Le document store chargé ou None.
        """
        cache_path = self._get_cache_path(f"document_store_{data_hash}.pkl")
        try:
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    document_store = pickle.load(f)
                print(f"✅ Document store chargé depuis le cache: {cache_path}")
                return document_store
            else:
                print("⚠️  Cache document store non trouvé")
                return None
        except Exception as e:
            print(f"❌ Erreur chargement document store: {e}")
            return None

    def save_embeddings(self, embeddings: Dict[str, Any], data_hash: str) -> None:
        """
        Sauvegarde les embeddings dans le cache.
        Args:
            embeddings (Dict[str, Any]): Embeddings à sauvegarder.
            data_hash (str): Hash des données pour versionner le cache.
        """
        cache_path = self._get_cache_path(f"embeddings_{data_hash}.pkl")
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(embeddings, f)
            print(f"✅ Embeddings sauvegardés: {cache_path}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde embeddings: {e}")

    def load_embeddings(self, data_hash: str) -> Optional[Dict[str, Any]]:
        """
        Charge les embeddings depuis le cache.
        Args:
            data_hash (str): Hash des données pour versionner le cache.
        Returns:
            Optional[Dict[str, Any]]: Embeddings chargés ou None.
        """
        cache_path = self._get_cache_path(f"embeddings_{data_hash}.pkl")
        try:
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    embeddings = pickle.load(f)
                print(f"✅ Embeddings chargés depuis le cache: {cache_path}")
                return embeddings
            else:
                print("⚠️  Cache embeddings non trouvé")
                return None
        except Exception as e:
            print(f"❌ Erreur chargement embeddings: {e}")
            return None

    def save_retriever(self, retriever: BM25Retriever, data_hash: str) -> None:
        """
        Sauvegarde un retriever BM25 dans le cache.
        Args:
            retriever (BM25Retriever): Retriever à sauvegarder.
            data_hash (str): Hash des données pour versionner le cache.
        """
        cache_path = self._get_cache_path(f"retriever_{data_hash}.pkl")
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(retriever, f)
            print(f"✅ Retriever sauvegardé: {cache_path}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde retriever: {e}")

    def load_retriever(self, data_hash: str) -> Optional[BM25Retriever]:
        """
        Charge un retriever BM25 depuis le cache.
        Args:
            data_hash (str): Hash des données pour versionner le cache.
        Returns:
            Optional[BM25Retriever]: Retriever chargé ou None.
        """
        cache_path = self._get_cache_path(f"retriever_{data_hash}.pkl")
        try:
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    retriever = pickle.load(f)
                print(f"✅ Retriever chargé depuis le cache: {cache_path}")
                return retriever
            else:
                print("⚠️  Cache retriever non trouvé")
                return None
        except Exception as e:
            print(f"❌ Erreur chargement retriever: {e}")
            return None

    def clear_cache(self) -> None:
        """
        Efface tous les fichiers du cache.
        """
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("✅ Cache effacé")
        except Exception as e:
            print(f"❌ Erreur effacement cache: {e}")

    def get_cache_info(self) -> Dict[str, Any]:
        """
        Retourne des informations sur le cache (nombre de fichiers, taille totale, etc.).
        Returns:
            Dict[str, Any]: Infos sur le cache.
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
            print(f"❌ Erreur lecture cache info: {e}")
        return cache_info

# Instance globale
model_cache = ModelCache()