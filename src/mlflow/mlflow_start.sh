#!/bin/bash

# Chargement de la config 'models' initiale si aucune définie
if [ -d "/mlruns" ]; then
    echo "Le dossier /mlruns existe déjà."
else
    echo "Le dossier /mlruns n'existe pas. Chargement de la config initiale"
    cp -r /app/src/config/mlruns_init /mlruns
fi

# Démarrer le serveur MLflow en arrière-plan
mlflow server --host 0.0.0.0 --port 5000 --default-artifact-root ./mlruns &

# Se positionner dans le bon dossier
cd ./app/src/mlflow/

# Démarrer l'API FastAPI
python3 mlf_api.py