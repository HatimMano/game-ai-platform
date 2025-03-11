import pickle
import os
from models.model_manager import BaseModelManager

class QLearningManager(BaseModelManager):
    """Gestionnaire pour les modèles Q-Learning."""

    def save_model(self, q_table, model_path):
        """Sauvegarde le modèle Q-Learning dans un fichier pickle."""
        with open(model_path, "wb") as f:
            pickle.dump(dict(q_table), f)

    def load_model(self, model_path):
        """Charge le modèle Q-Learning depuis un fichier pickle."""
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                try:
                    return pickle.load(f)
                except (EOFError, pickle.UnpicklingError):
                    print(f"Erreur lors du chargement du modèle {model_path}. Le fichier est corrompu.")
                    return {}

        else:
            print(f"Modèle introuvable : {model_path}. Initialisation d'une nouvelle Q-table.")
            return {}
