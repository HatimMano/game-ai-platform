from abc import ABC, abstractmethod

class BaseAgent:
    def __init__(self, env):
        self.env = env

    @abstractmethod
    def train(self, num_episodes):
        """Entraîne l'agent sur un certain nombre d'épisodes."""
        pass

    @abstractmethod
    def choose_action(self, state, epsilon):
        """Sélectionne une action en fonction de l'état et de la politique d'exploration."""
        pass

    @abstractmethod
    def set_model(self, model):
        """Charge un modèle dans l'agent."""
        pass


