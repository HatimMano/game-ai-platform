from abc import ABC, abstractmethod

class BaseAgent:
    def __init__(self, env):
        self.env = env

    def load_model(self, model_path):
        """Charge un modèle selon l'implémentation spécifique de l'agent."""
        pass

    @abstractmethod
    def train(self, num_episodes):
        """Entraîne l'agent sur un certain nombre d'épisodes."""
        pass

    @abstractmethod
    def choose_action(self, state, epsilon):
        """Sélectionne une action en fonction de l'état et de la politique d'exploration."""
        pass

    @abstractmethod
    def load(self, model_path):
        """Méthode générique pour charger le modèle"""
        pass
