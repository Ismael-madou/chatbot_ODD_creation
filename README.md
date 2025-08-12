# Chatbot ODD (Objectifs de Développement Durable)

Ce projet est une application Streamlit moderne et bilingue (français/anglais) permettant d'explorer, questionner et sensibiliser autour des 17 Objectifs de Développement Durable (ODD) de l'ONU.
## Fonctionnalités principales
- **Interface moderne et responsive** (Streamlit)
- **Bilingue** : tout le contenu, les titres, les suggestions, les réponses et les tableaux sont dynamiques et changent de langue instantanément
- **Cartes ODD compactes** : affichage de tous les ODD avec description, suggestions et liens
- **Recherche intelligente** : moteur sémantique (SentenceTransformer) et BM25 pour retrouver les ODD pertinents
- **Réponses reformulées** par LLM (transformers)
- **Quiz interactif** sur les ODD
- **Mode accessibilité** (contraste élevé)
- **Feedback utilisateur**
- **Téléchargement CSV de l’historique**
- **Gestion d’état robuste** : tout le contenu s’adapte à la langue, aucun mélange, un seul sélecteur de langue

## Structure du projet
- `app.py` : interface Streamlit principale
- `chat_bot.py` : logique de recherche, LLM, gestion multilingue
- `llm_integration.py` : intégration du modèle de langage
- `model_cache.py` : gestion du cache d’embeddings et du retriever
- `odd_data_enriched_bilingual.json` : données ODD enrichies, bilingues et valides
- `requirements.txt` : dépendances Python

## Lancer l’application
1. Crée un environnement virtuel et installe les dépendances :
	```powershell
	python -m venv venv
	.\venv\Scripts\activate
	pip install -r requirements.txt
	```
2. Lance Streamlit :
	```powershell
	streamlit run app.py
	```

## Dépôt Git
- Les fichiers non essentiels (venv, cache, images, etc.) sont exclus via `.gitignore`.
- Seuls les scripts, données JSON, et README sont suivis.

## Auteurs
- Ismael Madou
- Contributions bienvenues !
<<<<<<< HEAD

# 🌍 SDG-Bot – Smart Awareness Chatbot for the Sustainable Development Goals

> Empowering youth with knowledge, action, and inspiration through the United Nations 2030 Agenda.

---

## 🧭 Project Overview

**SDG-Bot** is an intelligent and interactive chatbot designed to raise awareness about the 17 Sustainable Development Goals (SDGs) set by the United Nations. It aims to educate young people in an engaging, accessible, and multilingual way by answering common questions, offering region-specific insights, and providing guidance on how to take action.

---

## ✨ Key Features

- ✅ Instant answers to frequently asked questions (e.g., “How many SDGs exist?”, “Which agency is responsible for SDG 4?”)
- 🌐 Region-aware recommendations (Africa, Europe, Asia, America, Oceania)
- 🧠 Lightweight Natural Language Processing for basic intent recognition
- 📚 Easily extendable JSON-based knowledge base
- 🎯 Future-ready for quiz modules, stats, and action tracking
- 🔗 API-ready architecture to connect with UN or SDG data platforms

---

## 🧱 Project Structure

# 🌍 SDG-Bot – Smart Awareness Chatbot for the Sustainable Development Goals

> Empowering youth with knowledge, action, and inspiration through the United Nations 2030 Agenda.

---

## 🧭 Project Overview

**SDG-Bot** is an intelligent and interactive chatbot designed to raise awareness about the 17 Sustainable Development Goals (SDGs) set by the United Nations. It aims to educate young people in an engaging, accessible, and multilingual way by answering common questions, offering region-specific insights, and providing guidance on how to take action.

---

## ✨ Key Features

- ✅ Instant answers to frequently asked questions (e.g., “How many SDGs exist?”, “Which agency is responsible for SDG 4?”)
- 🌐 Region-aware recommendations (Africa, Europe, Asia, America, Oceania)
- 🧠 Lightweight Natural Language Processing for basic intent recognition
- 📚 Easily extendable JSON-based knowledge base
- 🎯 Future-ready for quiz modules, stats, and action tracking
- 🔗 API-ready architecture to connect with UN or SDG data platforms

---

## 📁 Project Structure

```bash
sdg_bot/
│
├── data/
│   └── sdg_faq.json            # Core knowledge base of Q&A about SDGs
│
├── chatbot.py                  # Command-line chatbot logic
├── quiz_module.py              # (Optional) Interactive SDG quiz logic
├── region_filter.py            # (Optional) Regional SDG analysis
├── api_connector.py            # (Future) External UN API integration
└── README.md                   # Project documentation
=======
# Chatbot ODD avec IA 🌍

Un chatbot intelligent spécialisé dans les Objectifs de Développement Durable (ODD) utilisant l'IA avancée pour fournir des réponses naturelles et engageantes.

## 🚀 Fonctionnalités

- **Recherche intelligente** : Utilise Haystack et Sentence Transformers pour trouver les informations pertinentes
- **Réponses naturelles** : Intégration LLM (OpenAI) pour des réponses fluides et contextuelles
- **Interface moderne** : Interface Streamlit avec chat en temps réel
- **Données enrichies** : Base de connaissances complète sur les 17 ODD
- **Mode fallback** : Fonctionne même sans clé API OpenAI
- **⚡ Chargement rapide** : Système de cache PKL pour accélérer le démarrage

## 🛠️ Installation

### Méthode recommandée (automatique)
```bash
# Cloner le repository
git clone <repository-url>
cd chatbot_ODD_creation

# Installation automatique avec résolution des conflits
python install.py
```

### Méthode manuelle
1. **Cloner le repository**
```bash
git clone <repository-url>
cd chatbot_ODD_creation
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configuration OpenAI (optionnel)**
```bash
# Créer un fichier .env
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

4. **Initialiser le cache (recommandé)**
```bash
python cache_manager.py init
```

## 🔧 Dépannage

### Erreur de dépendances (pydantic/haystack)
Si vous rencontrez l'erreur `ImportError: cannot import name 'TypeAdapter' from 'pydantic'`, utilisez le script d'installation automatique :

```bash
python install.py
```

Ce script va :
- Désinstaller les versions conflictuelles
- Installer les bonnes versions dans le bon ordre
- Résoudre automatiquement les conflits

### Réinstallation complète
Si les problèmes persistent :
```bash
# Désinstaller toutes les dépendances
pip uninstall -y pydantic haystack-ai sentence-transformers streamlit openai python-dotenv torch transformers numpy pandas

# Réinstaller avec le script automatique
python install.py
```

## 🎯 Utilisation

### Lancer l'application
```bash
streamlit run app.py
```

### Gestion du cache
```bash
# Voir les informations du cache
python cache_manager.py info

# Effacer le cache
python cache_manager.py clear

# Vérifier le statut du cache
python cache_manager.py status

# Forcer la régénération du cache
python cache_manager.py init --force
```

### Utilisation sans LLM
Le chatbot fonctionne parfaitement sans clé OpenAI, en utilisant le mode fallback avec les réponses formatées.

### Utilisation avec LLM
Avec une clé OpenAI valide, le chatbot génère des réponses plus naturelles et contextuelles.

## 📁 Structure du projet

```
chatbot_ODD_creation/
├── app.py                 # Interface Streamlit principale
├── chat_bot.py           # Logique de recherche et traitement
├── llm_integration.py    # Intégration LLM OpenAI
├── model_cache.py        # Système de cache PKL
├── cache_manager.py      # Script de gestion du cache
├── install.py            # Script d'installation automatique
├── haystack_integration.py # Configuration Haystack
├── odd_data_enriched.json # Base de connaissances ODD
├── requirements.txt      # Dépendances Python
├── cache/                # Répertoire de cache (généré automatiquement)
├── logo_ODD.PNG         # Logo de l'application
└── objectifs_ODD.PNG    # Image des ODD
```

## 🔧 Configuration

### Variables d'environnement
- `OPENAI_API_KEY` : Votre clé API OpenAI (optionnel)
- `OPENAI_MODEL` : Modèle à utiliser (défaut: gpt-3.5-turbo)

### Modèles supportés
- `gpt-3.5-turbo` (recommandé)
- `gpt-4` (si disponible)
- Mode fallback (sans API key)

### Versions compatibles
- `pydantic==1.10.13` (version fixe pour éviter les conflits)
- `haystack-ai>=1.0.0`
- `sentence-transformers>=2.2.0`

## ⚡ Performance

### Système de cache PKL
Le chatbot utilise un système de cache intelligent qui sauvegarde :
- **Modèles pré-chargés** : SentenceTransformer
- **Document store** : Haystack InMemoryDocumentStore
- **Retriever** : BM25Retriever
- **Embeddings** : Vecteurs pré-calculés

### Avantages du cache
- **🚀 Démarrage rapide** : De ~30 secondes à ~2 secondes
- **💾 Économie de bande passante** : Pas de re-téléchargement des modèles
- **🔧 Calculs optimisés** : Embeddings pré-calculés
- **🔄 Gestion intelligente** : Cache automatique avec vérification d'intégrité

### Gestion du cache
- **Interface utilisateur** : Boutons dans la sidebar pour gérer le cache
- **Script CLI** : `cache_manager.py` pour la gestion avancée
- **Auto-détection** : Le cache est automatiquement utilisé s'il existe

## 🎨 Interface utilisateur

- **Chat en temps réel** : Interface moderne avec historique des conversations
- **Recherche intelligente** : Trouve automatiquement les informations pertinentes
- **Réponses contextuelles** : Adapte les réponses à la question posée
- **Interface responsive** : Fonctionne sur desktop et mobile
- **Gestion du cache** : Interface intégrée pour gérer les performances

## 📊 Données

Le chatbot utilise une base de connaissances enrichie contenant :
- **17 ODD** avec descriptions détaillées
- **Statistiques** actuelles et chiffres clés
- **Cibles** spécifiques pour chaque ODD
- **Actions concrètes** que chacun peut entreprendre
- **FAQ** complète sur les ODD

## 🤖 Technologies utilisées

- **Streamlit** : Interface utilisateur
- **Haystack** : Recherche d'information
- **Sentence Transformers** : Embeddings et similarité
- **OpenAI API** : Génération de réponses naturelles
- **Python-dotenv** : Gestion des variables d'environnement
- **Pickle** : Système de cache PKL

## 🔄 Améliorations récentes

### Phase 2 - Intégration LLM
- ✅ Suppression des questions dans les réponses
- ✅ Intégration OpenAI pour des réponses naturelles
- ✅ Interface de chat moderne
- ✅ Mode fallback robuste
- ✅ Gestion d'erreurs améliorée

### Phase 3 - Optimisation Performance
- ✅ Système de cache PKL
- ✅ Chargement rapide des modèles
- ✅ Pré-calcul des embeddings
- ✅ Interface de gestion du cache
- ✅ Script CLI pour la maintenance

### Phase 4 - Résolution des conflits
- ✅ Script d'installation automatique
- ✅ Versions compatibles des dépendances
- ✅ Gestion des conflits pydantic/haystack
- ✅ Documentation de dépannage

## 🚀 Déploiement

### Local
```bash
# Installation et initialisation
python install.py
python cache_manager.py init
streamlit run app.py
```

### Cloud (Streamlit Cloud)
1. Connecter votre repository GitHub
2. Configurer les variables d'environnement
3. Le cache sera généré automatiquement au premier démarrage
4. Déployer automatiquement

## 📝 Exemples d'utilisation

- "Qu'est-ce que l'ODD 1 ?"
- "Comment lutter contre le changement climatique ?"
- "Que sont les ODD ?"
- "Comment puis-je contribuer aux ODD ?"
- "Quels sont les défis principaux ?"

## 🔧 Maintenance

### Gestion du cache
```bash
# Vérifier l'état du cache
python cache_manager.py status

# Nettoyer le cache si nécessaire
python cache_manager.py clear

# Régénérer le cache
python cache_manager.py init --force
```

### Performance
- Le cache est automatiquement invalidé si les données changent
- Les fichiers de cache sont compressés et optimisés
- Le système vérifie l'intégrité des données

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📄 Licence

Ce projet est sous licence MIT.

## 🔗 Liens utiles

- [Objectifs de Développement Durable](https://www.un.org/sustainabledevelopment/fr/)
- [OpenAI API](https://platform.openai.com/)
- [Streamlit](https://streamlit.io/)
- [Haystack](https://haystack.deepset.ai/)
>>>>>>> 64aa8d4 (Ajout d'un .gitignore pour exclure les fichiers non essentiels)
