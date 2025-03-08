import pytest # type: ignore
import os
from models.q_learning.train import agent, model_path
from models.model_manager import ModelManager

def test_training():
    assert os.path.exists(model_path)  # Vérifie que le modèle a bien été sauvegardé après l'entraînement
    q_table = ModelManager.load_q_table(model_path)
    assert isinstance(q_table, dict)  # Vérifie que la Q-table a bien été chargée
