# 1. Image de base officielle (version figée)
FROM python:3.12-slim

# 2. Dossier de travail dans le conteneur
WORKDIR /app

# 3. Dépendances d'abord, Docker met cette couche en cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# 4. le code des developpeurs
COPY app.py .


# 5. Sécurité (on ne tourne pas en root)
RUN  useradd -m appuser

USER appuser

# 6. Documentation du port commande de demarrage
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]



