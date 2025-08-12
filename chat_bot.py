"""
chat_bot.py - Logique principale du Chatbot ODD

Ce module gère la logique de recherche, le matching, le fallback, la gestion du cache et l'intégration avec Haystack et Sentence Transformers.

Fonctions principales :
- initialize_chatbot : Initialise tous les modèles, données et caches nécessaires.
- chercher_odd : Recherche la réponse la plus pertinente à une question utilisateur.
- formater_reponse_odd : Formate la réponse à afficher à l'utilisateur.
- clear_cache : Vide le cache local.
- get_cache_info : Retourne des infos sur le cache.

Variables globales :
- model, document_store, retriever, odds, faq, odd_documents, odd_embeddings
"""
import json
import re
import os
import time
from typing import Any, Dict, Optional, List, Union

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    SentenceTransformer = None
    util = None
try:
    from haystack.document_stores import InMemoryDocumentStore
    from haystack.nodes import BM25Retriever
except ImportError:
    InMemoryDocumentStore = None
    BM25Retriever = None
try:
    from transformers import pipeline
except ImportError:
    pipeline = None

try:
    from llm_integration import llm_integration
except ImportError:
    llm_integration = None
try:
    from model_cache import model_cache
except ImportError:
    model_cache = None

# Variables globales pour les modèles et données
model: Optional[Any] = None
document_store: Optional[Any] = None
retriever: Optional[Any] = None
odds: Optional[List[Dict[str, Any]]] = None
faq: Optional[List[Dict[str, Any]]] = None
odd_documents: Optional[List[str]] = None
odd_embeddings: Any = None

# Charger le pipeline LLM local une seule fois
_llm_pipeline = None
def get_llm_pipeline() -> any:
    """
    Charge et retourne le pipeline LLM local (modèle text2text-generation).
    Returns:
        pipeline ou None : pipeline transformers prêt à l'emploi ou None si indisponible.
    """
    global _llm_pipeline
    if pipeline is None:
        print("[ERREUR] transformers n'est pas installé. Réponse LLM désactivée.")
        return None
    if _llm_pipeline is None:
        try:
            # Modèle ultra-léger pour CPU
            _llm_pipeline = pipeline("text2text-generation", model="google/flan-t5-small", device=-1)
        except Exception as e:
            print(f"[ERREUR] Impossible de charger le pipeline LLM: {e}")
            _llm_pipeline = None
    return _llm_pipeline

def generer_reponse_llm(question: str) -> str:
    """
    Génère une réponse à partir d'une question en utilisant le pipeline LLM local.
    Args:
        question (str): La question utilisateur.
    Returns:
        str: Réponse générée ou message d'erreur.
    """
    pipe = get_llm_pipeline()
    if pipe is None:
        return "[ERREUR] LLM non disponible."
    try:
        result = pipe(question, max_new_tokens=64, do_sample=True)
        return result[0].get('generated_text', str(result[0]))
    except Exception as e:
        return f"[ERREUR LLM] {e}"

def initialize_chatbot() -> None:
    """
    Initialise le chatbot avec le système de cache pour accélérer le chargement.
    Charge les données, le modèle, le document store, le retriever et les embeddings.
    Variables globales modifiées : model, document_store, retriever, odds, faq, odd_documents, odd_embeddings
    """
    """
    Initialise le chatbot avec le système de cache pour accélérer le chargement.
    Charge les données, le modèle, le document store, le retriever et les embeddings.
    """
    global model, document_store, retriever, odds, faq, odd_documents, odd_embeddings
    print("🚀 Initialisation du chatbot ODD...")
    start_time = time.time()
    # Chargement des données ODD et FAQ enrichies
    data_path = os.path.join(os.path.dirname(__file__), "odd_data_enriched.json")
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        odds = data.get("odds", [])
        faq = data.get("faq", [])
    except Exception as e:
        print(f"❌ Fichier de données introuvable ou corrompu : {data_path}\nErreur : {e}")
        odds = []
        faq = []
    if not odds:
        print("[ERREUR] Aucune donnée ODD chargée. Le chatbot ne pourra pas répondre correctement.")
    # Générer le hash des données pour le cache
    if model_cache and hasattr(model_cache, '_get_data_hash'):
        data_hash = model_cache._get_data_hash({"odds": odds, "faq": faq})
    else:
        data_hash = "nohash"
    # Tentative de chargement du modèle depuis le cache
    if model_cache and hasattr(model_cache, 'load_model'):
        print("🤖 Chargement du modèle SentenceTransformer...")
        model = model_cache.load_model()
    else:
        model = None
    if model is None and SentenceTransformer is not None:
        try:
            print("📥 Téléchargement du modèle ultra-léger depuis HuggingFace...")
            model = SentenceTransformer("all-MiniLM-L6-v2")
            if model_cache and hasattr(model_cache, 'save_model'):
                model_cache.save_model(model)
        except Exception as e:
            print(f"[ERREUR] Impossible de charger le modèle SentenceTransformer : {e}")
            model = None
    if model is None:
        print("[ERREUR] SentenceTransformer non disponible. Les recherches avancées sont désactivées.")
    # Tentative de chargement du document store depuis le cache
    if model_cache and hasattr(model_cache, 'load_document_store'):
        print("📚 Chargement du document store...")
        document_store = model_cache.load_document_store(data_hash)
    else:
        document_store = None
    if document_store is None and InMemoryDocumentStore is not None:
        try:
            print("🔨 Création du document store...")
            document_store = create_haystack_store()
            if model_cache and hasattr(model_cache, 'save_document_store'):
                model_cache.save_document_store(document_store, data_hash)
        except Exception as e:
            print(f"[ERREUR] Impossible de créer le document store : {e}")
            document_store = None
    # Tentative de chargement du retriever depuis le cache
    if model_cache and hasattr(model_cache, 'load_retriever'):
        print("🔍 Chargement du retriever...")
        retriever = model_cache.load_retriever(data_hash)
    else:
        retriever = None
    if retriever is None and BM25Retriever is not None and document_store is not None:
        try:
            print("🔨 Création du retriever...")
            retriever = BM25Retriever(document_store=document_store, top_k=3)
            if model_cache and hasattr(model_cache, 'save_retriever'):
                model_cache.save_retriever(retriever, data_hash)
        except Exception as e:
            print(f"[ERREUR] Impossible de créer le retriever : {e}")
            retriever = None
    # Pré-calculer les embeddings pour les ODD (fallback)
    if model_cache and hasattr(model_cache, 'load_embeddings'):
        print("🧮 Pré-calcul des embeddings...")
        embeddings_cache = model_cache.load_embeddings(data_hash)
    else:
        embeddings_cache = None
    if embeddings_cache is None and model is not None and odds:
        try:
            print("🔨 Calcul des embeddings...")
            odd_documents = [f"ODD {d['odd']}: {d['title']} - {d['description']} - {' '.join(d.get('keywords', []))}" for d in odds]
            embeddings_cache = {
                "documents": odd_documents,
                "embeddings": model.encode(odd_documents, convert_to_tensor=True)
            }
            if model_cache and hasattr(model_cache, 'save_embeddings'):
                model_cache.save_embeddings(embeddings_cache, data_hash)
        except Exception as e:
            print(f"[ERREUR] Impossible de calculer les embeddings : {e}")
            embeddings_cache = {"documents": [], "embeddings": []}
    if embeddings_cache:
        odd_documents = embeddings_cache.get("documents", [])
        odd_embeddings = embeddings_cache.get("embeddings", [])
    elapsed_time = time.time() - start_time
    print(f"✅ Chatbot initialisé en {elapsed_time:.2f} secondes")
    # Afficher les informations du cache
    if model_cache and hasattr(model_cache, 'get_cache_info'):
        cache_info = model_cache.get_cache_info()
        print(f"📊 Cache: {cache_info.get('file_count', 0)} fichiers, {cache_info.get('total_size_mb', 0)} MB")

def create_haystack_store() -> Any:
    """
    Crée et retourne un InMemoryDocumentStore Haystack à partir des données ODD et FAQ chargées.
    Returns:
        InMemoryDocumentStore ou None : Le document store prêt à l'emploi ou None si indisponible.
    """
    """
    Crée et retourne un InMemoryDocumentStore Haystack à partir des données ODD et FAQ chargées.
    Retourne :
        InMemoryDocumentStore : Le document store prêt à l'emploi.
    """
    if InMemoryDocumentStore is None:
        print("[ERREUR] Haystack n'est pas installé. Document store désactivé.")
        return None
    documents = []
    # Documents ODD enrichis
    for odd in odds or []:
        try:
            doc_text = f"ODD {odd['odd']}: {odd['title']}. {odd['description']}. "
            doc_text += f"Statistiques: {odd.get('statistics', '')}. "
            doc_text += f"Mots-clés: {', '.join(odd.get('keywords', []))}. "
            if odd.get('cibles'):
                cibles_text = "; ".join([f"{c.get('code', '')}: {c.get('description', '')}" for c in odd.get('cibles', [])])
                doc_text += f"Cibles: {cibles_text}. "
            if odd.get('actions'):
                actions_text = "; ".join(odd.get('actions', []))
                doc_text += f"Actions: {actions_text}."
            documents.append({
                "content": doc_text,
                "meta": {
                    "odd_number": odd.get("odd", ""),
                    "title": odd.get("title", ""),
                    "description": odd.get("description", ""),
                    "keywords": odd.get("keywords", []),
                    "statistics": odd.get("statistics", ""),
                    "related_odds": odd.get("related_odds", []),
                    "cibles": odd.get("cibles", []),
                    "actions": odd.get("actions", []),
                    "type": "odd"
                }
            })
        except Exception as e:
            print(f"[ERREUR] Impossible d'ajouter un ODD au document store : {e}")
    # Documents FAQ enrichis
    for faq_item in faq or []:
        try:
            doc_text = f"{faq_item.get('answer', '')}"
            if faq_item.get('keywords'):
                doc_text += f" Mots-clés: {', '.join(faq_item.get('keywords', []))}"
            documents.append({
                "content": doc_text,
                "meta": {
                    "type": "faq",
                    "question": faq_item.get("question", ""),
                    "answer": faq_item.get("answer", ""),
                    "keywords": faq_item.get("keywords", []),
                    "category": faq_item.get("category", "général")
                }
            })
        except Exception as e:
            print(f"[ERREUR] Impossible d'ajouter une FAQ au document store : {e}")
    document_store = InMemoryDocumentStore(use_bm25=True)
    document_store.write_documents(documents)
    return document_store

def chercher_odd(question: str, lang: str = "Français") -> Dict[str, Any]:
    """
    Recherche l'ODD ou la FAQ la plus pertinente pour la question donnée, version bilingue.
    Args:
        question (str): La question de l'utilisateur.
        lang (str): "English" ou "Français".
    Returns:
        Dict[str, Any]: Les données de l'ODD ou de la FAQ la plus pertinente.
    """
    if not odds:
        print("[LOG] Aucune donnée ODD disponible.")
        return {"error": "Aucune donnée ODD disponible."}
    match = re.search(r"odd\s*(\d+)", question.lower())
    if match:
        num = int(match.group(1))
        for d in odds:
            if d.get("odd") == num:
                return d
    if question.strip().isdigit():
        num = int(question.strip())
        for d in odds:
            if d.get("odd") == num:
                return d
    # Recherche BM25 (recherche sémantique sur le texte)
    if retriever is not None:
        try:
            results = retriever.retrieve(query=question, top_k=3)
        except Exception as e:
            print(f"[ERREUR] Recherche BM25 échouée : {e}")
            results = []
        if results:
            best_result = results[0]
            if best_result.meta.get("type") == "odd":
                return best_result.meta
            elif best_result.meta.get("type") == "faq":
                return best_result.meta
    # Recherche par mots-clés dynamiques (bilingue)
    question_lower = question.lower()
    for odd in odds:
        for keyword in odd.get("keywords", {}).get("en" if lang == "English" else "fr", []):
            if keyword.lower() in question_lower:
                return odd
    for faq_item in faq or []:
        for keyword in faq_item.get("keywords", {}).get("en" if lang == "English" else "fr", []):
            if keyword.lower() in question_lower:
                # On retourne une structure FAQ bilingue compatible
                return {
                    "type": "faq",
                    "question": faq_item.get("question", {}),
                    "answer": faq_item.get("answer", {}),
                    "keywords": faq_item.get("keywords", {}),
                    "category": faq_item.get("category", "général")
                }
    # Recherche sémantique par embeddings (fallback)
    if model is not None and util is not None and odd_embeddings is not None and odds:
        try:
            question_embedding = model.encode(question, convert_to_tensor=True)
            scores = util.pytorch_cos_sim(question_embedding, odd_embeddings)[0]
            best_match_idx = scores.argmax()
            return odds[best_match_idx]
        except Exception as e:
            print(f"[ERREUR] Recherche par embeddings échouée : {e}")
    return {"error": "Aucune correspondance trouvée pour la question."}

def formater_reponse_odd(odd_data: Dict[str, Any], question: str = "", lang: str = "Français") -> str:
    """
    Formate la réponse pour un ODD ou une FAQ avec toutes les données enrichies, version bilingue.
    Args:
        odd_data (Dict[str, Any]): Les données de l'ODD ou de la FAQ.
        question (str): La question de l'utilisateur (pour le prompt LLM).
        lang (str): "English" ou "Français".
    Returns:
        str: La réponse formatée à afficher.
    """
    if odd_data.get("error"):
        return f"[ERROR] {odd_data['error']}" if lang == "English" else f"[ERREUR] {odd_data['error']}"
    # Formatage ODD ou FAQ brut bilingue
    if odd_data.get("type") == "faq":
        q = odd_data.get('question', {})
        a = odd_data.get('answer', {})
        question_txt = q.get('en', q) if lang == 'English' else q.get('fr', q)
        answer_txt = a.get('en', a) if lang == 'English' else a.get('fr', a)
        base = f"FAQ: {question_txt}\n"
        base += f"Answer: {answer_txt}" if lang == "English" else f"Réponse : {answer_txt}"
    else:
        title = odd_data.get('title', {})
        desc = odd_data.get('description', {})
        stats = odd_data.get('statistics', {})
        actions = odd_data.get('actions', {})
        base = f"{'SDG' if lang == 'English' else 'ODD'} {odd_data.get('odd', '')} : {title.get('en', title) if lang == 'English' else title.get('fr', title)}\n"
        base += f"{desc.get('en', desc) if lang == 'English' else desc.get('fr', desc)}"
        if stats:
            stat_txt = stats.get('en', stats) if lang == 'English' else stats.get('fr', stats)
            base += f"\n{'Statistics' if lang == 'English' else 'Statistiques'} : {stat_txt}"
        if odd_data.get('cibles'):
            cibles = ", ".join([
                f"{c.get('code', '')}: {c.get('description', {}).get('en', c.get('description', '')) if lang == 'English' else c.get('description', {}).get('fr', c.get('description', ''))}"
                for c in odd_data.get('cibles', [])
            ])
            base += f"\n{'Targets' if lang == 'English' else 'Cibles'} : {cibles}"
        if actions:
            act_list = actions.get('en', actions) if lang == 'English' else actions.get('fr', actions)
            if isinstance(act_list, list):
                base += f"\n{'Actions' if lang == 'English' else 'Actions'} : {', '.join(act_list)}"
            else:
                base += f"\n{'Actions' if lang == 'English' else 'Actions'} : {act_list}"
    # Optionnel : reformulation LLM si dispo
    if llm_integration and hasattr(llm_integration, 'generate_response'):
        try:
            if lang == "English":
                prompt = f"Here is information about an SDG or FAQ:\n{base}\n\nUser question: {question}\n\nWrite a clear and concise answer for a human in English."
            else:
                prompt = f"Voici des informations sur un ODD ou une FAQ :\n{base}\n\nQuestion utilisateur : {question}\n\nFais une réponse claire et synthétique pour un humain en français."
            llm_resp = llm_integration.generate_response(prompt)
            if llm_resp and isinstance(llm_resp, str) and len(llm_resp.strip()) > 10:
                return f"{base}\n\n{'🤖 AI reformulation:' if lang == 'English' else '🤖 Reformulation IA :'}\n{llm_resp.strip()}"
        except Exception as e:
            return f"{base}\n[LLM ERROR] {e}" if lang == "English" else f"{base}\n[ERREUR LLM integration] {e}"
    return base

def clear_cache() -> None:
    """
    Efface le cache pour forcer le rechargement des modèles et données.
    """
    """
    Efface le cache pour forcer le rechargement des modèles et données.
    """
    if model_cache and hasattr(model_cache, 'clear_cache'):
        model_cache.clear_cache()
        print("🗑️ Cache effacé. Le prochain démarrage sera plus lent.")
    else:
        print("[ERREUR] Impossible d'effacer le cache : model_cache non disponible.")

def get_cache_info() -> Dict[str, Any]:
    """
    Retourne les informations sur le cache actuel (nombre de fichiers, taille, etc.).
    Returns:
        Dict[str, Any]: Informations sur le cache.
    """
    """
    Retourne les informations sur le cache actuel (nombre de fichiers, taille, etc.).
    Returns:
        Dict[str, Any]: Informations sur le cache.
    """
    if model_cache and hasattr(model_cache, 'get_cache_info'):
        return model_cache.get_cache_info()
    return {"error": "model_cache non disponible"}

# Initialisation automatique au chargement du module
initialize_chatbot()