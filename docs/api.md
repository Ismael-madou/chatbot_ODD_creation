# Structure & API

## Organisation du projet

- `main.py` : point d’entrée unique
- `src/app.py` : interface Streamlit
- `src/chat_bot.py` : logique de recherche, LLM, multilingue
- `src/model_cache.py` : gestion du cache
- `src/sdg_data.py` : accès aux données Excel
- `data/` : fichiers de données (Excel, JSON)
- `pictures/` : images et logos
- `cache/` : fichiers de cache générés automatiquement

## Fonctions principales

- `chercher_odd(question, lang)` : recherche la réponse la plus pertinente à une question utilisateur
- `formater_reponse_odd(result, question, lang)` : formate la réponse pour l’affichage
- `clear_cache()` : efface le cache
- `get_cache_info()` : retourne des infos sur le cache

## Exemples d’utilisation

```python
from src.chat_bot import chercher_odd
result = chercher_odd("Qu'est-ce que l'ODD 1 ?", lang="Français")
print(result)
```
