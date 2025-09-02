# FAQ

## Quelle version de Python utiliser ?

Il est recommandé d’utiliser **la même version de Python que celle de votre environnement virtuel** pour garantir la compatibilité avec les dépendances (voir `requirements.txt`).

- Pour vérifier la version de votre environnement virtuel :
  ```bash
  python --version
  ```
- Pour créer un environnement virtuel avec une version spécifique :
  ```bash
  python3.10 -m venv .venv
  ```

## Comment lancer le projet ?

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Lancez l’application :
   ```bash
   python main.py
   ```

## Comment générer la documentation ?

```bash
mkdocs serve
```

## Où sont stockées les données ?

- Données Excel et JSON : `data/`
- Images : `pictures/`
- Cache : `cache/`

## Comment vider le cache ?

Utilisez la fonction `clear_cache()` du module `model_cache.py` ou supprimez le dossier `cache/`.

## Comment contribuer ?

- Forkez le repo, créez une branche, proposez une PR.
- Respectez la structure du projet et les conventions de code.
- Ajoutez des tests et mettez à jour la documentation si besoin.
