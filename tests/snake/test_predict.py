import pytest # type: ignore
import os
import json
from models.q_learning.predict import predictions_path

def test_predictions():
    assert os.path.exists(predictions_path)  # Vérifie que le fichier `predictions.json` est bien généré

    with open(predictions_path, "r") as f:
        data = json.load(f)

    assert isinstance(data, list)  # Vérifie que les prédictions sont stockées sous forme de liste
    assert "episode" in data[0]  # Vérifie que chaque entrée a un numéro d'épisode
