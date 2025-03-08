import os
from importlib import import_module

class BaseModelManager:
    """Classe mère pour la gestion des modèles."""
    
    @staticmethod
    def get_manager_class(model_type):
        """Charge dynamiquement le gestionnaire de modèle en fonction du type."""
        module = import_module(f"models.{model_type}.{model_type}_manager")
        class_name = "".join(word.capitalize() for word in model_type.split("_")) + "Manager"
        manager_class = getattr(module, class_name)
        return manager_class

    
    def save_model(self, model, model_path):
        raise NotImplementedError("save_model doit être implémentée dans la classe fille")

    def load_model(self, model_path):
        raise NotImplementedError("load_model doit être implémentée dans la classe fille")
