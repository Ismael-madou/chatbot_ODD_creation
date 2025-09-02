# Guide d’utilisation

## 1. Installation

- Clonez le dépôt
- Créez un environnement virtuel Python (voir FAQ)
- Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## 2. Lancement

- Démarrez l’application :
   ```bash
   python main.py
   ```
- L’interface Streamlit s’ouvre dans votre navigateur

## 3. Utilisation

- Posez vos questions sur les ODD (en français ou anglais)
- Utilisez le menu pour changer de langue, télécharger les résultats, lancer un quiz, donner un feedback
- Les données sont extraites dynamiquement du fichier Excel

## 4. Tests & Qualité

- Lancer les tests :
   ```bash
   pytest
   ```
- Vérifier la qualité du code :
   ```bash
   flake8 src/
   ```

## 5. Documentation

- Générer la doc :
   ```bash
   mkdocs serve
   ```
- Accéder à la doc : http://localhost:8000

## 6. Déploiement

- Voir le guide `deploy.md` pour Docker et CI/CD
