# Déploiement & Production

## Docker

Le projet inclut un `Dockerfile` pour faciliter le déploiement :

```bash
docker build -t chatbot-odd .
docker run -p 8501:8501 chatbot-odd
```

## CI/CD

Des workflows GitHub Actions sont fournis :
- `python-tests.yml` : exécute les tests automatisés (pytest)
- `lint-python.yml` : vérifie la qualité du code (flake8)

## Conseils de production

- Utilisez un environnement virtuel dédié
- Vérifiez la version de Python (voir FAQ)
- Protégez les données sensibles (ne stockez pas de secrets dans le code)
- Surveillez l’espace disque pour le cache
- Pour un usage public, configurez un reverse proxy (Nginx, Traefik)

## Documentation

Générez la documentation avec :
```bash
mkdocs build
```
Le site statique sera dans `site/`.

## Support

Pour toute question, ouvrez une issue sur GitHub ou consultez la FAQ.
