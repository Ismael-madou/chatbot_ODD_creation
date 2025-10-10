
![Tests](https://github.com/Ismael-madou/chatbot_ODD_creation/actions/workflows/python-app.yml/badge.svg)

## ⚠️ Version de Python recommandée

Pour garantir la compatibilité des dépendances (notamment avec Streamlit, Haystack, Sentence Transformers, etc.), il est fortement conseillé d'utiliser la même version de Python que celle utilisée pour créer votre environnement virtuel.

- Vérifiez la version de Python de votre environnement virtuel avec :
	```powershell
	python --version
	```
- Si possible, utilisez Python 3.10 ou 3.11 (évitez les versions trop récentes ou trop anciennes qui peuvent causer des conflits de dépendances).

> Si vous rencontrez des erreurs d'import ou de compatibilité, vérifiez d'abord la version de Python utilisée dans votre venv.
# Chatbot ODD (Objectifs de Développement Durable)

Ce projet est une application Streamlit moderne, bilingue (français/anglais), permettant d'explorer, questionner et sensibiliser autour des 17 Objectifs de Développement Durable (ODD) de l'ONU.

## 🚀 Fonctionnalités principales
- **Interface moderne et responsive** (Streamlit)
- **Bilingue** : tout le contenu, les titres, suggestions, réponses et tableaux changent de langue instantanément
- **Cartes ODD dynamiques** : affichage de tous les ODD avec description, suggestions et liens
- **Recherche intelligente** : moteur sémantique (SentenceTransformer) et BM25 pour retrouver les ODD pertinents
- **Réponses reformulées** par LLM (transformers)
- **Quiz interactif** sur les ODD
- **Mode accessibilité** (contraste élevé)
- **Feedback utilisateur**
- **Téléchargement CSV de l’historique**
- **Gestion d’état robuste** : tout le contenu s’adapte à la langue, un seul sélecteur de langue
- **Classement ODD** : données pays issues d’un fichier Excel officiel, sans fallback statique
- **Système de cache** : accélère le démarrage après le premier lancement

## 📁 Structure du projet

```
chatbot_ODD_creation/
├── main.py                  # Point d'entrée unique (lance Streamlit ou le mode démo)
├── requirements.txt         # Dépendances Python
├── README.md                # Documentation
├── data/                    # Données (Excel, JSON)
│   ├── SDR2025-data.xlsx    # Données pays/classement ODD
│   └── odd_data_enriched_bilingual.json
├── pictures/                # Images (logos, ODD)
│   └── logo_ODD.png
├── cache/                   # Fichiers de cache générés automatiquement
└── src/                     # Code source principal
	├── app.py               # Interface Streamlit principale
	├── chat_bot.py          # Logique de recherche, LLM, multilingue
	├── llm_integration.py   # Intégration du modèle de langage
	├── model_cache.py       # Gestion du cache (modèles, embeddings, etc.)
	└── sdg_data.py          # Chargement et accès aux données Excel
```

## ⚡ Lancer l’application
1. Créez un environnement virtuel et installez les dépendances :
	```powershell
	python -m venv venv
	.\venv\Scripts\activate
	pip install -r requirements.txt
	```
2. Lancez l’application Streamlit (toujours depuis la racine du projet) :
	```powershell
	streamlit run main.py
	```
   > **Ne lancez jamais directement un fichier dans `src/`**

## 🗂️ Gestion du cache
- Le cache est généré automatiquement au premier lancement (modèles, embeddings, etc.)
- Les prochains démarrages sont très rapides
- Vous pouvez effacer le cache via le bouton dans la sidebar ou en supprimant le dossier `cache/`

## 📝 Bonnes pratiques
- Placez toutes vos données dans `data/` et vos images dans `pictures/`
- Modifiez uniquement `main.py` pour changer le point d’entrée
- Tous les chemins sont gérés automatiquement à partir de la racine du projet

## 👨‍💻 Auteurs
- Ismael Madou
- Abdoulaye Wade Toure
- Contributions bienvenues !
