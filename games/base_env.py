from abc import ABC, abstractmethod
import numpy as np

class BaseGameEnv(ABC):
    """Classe abstraite pour tous les environnements de jeu."""
    
    def __init__(self, grid_size=10):
        self.grid_size = grid_size

    @abstractmethod
    def reset(self):
        """Réinitialise l'environnement et retourne l'état initial."""
        pass

    @abstractmethod
    def step(self, action):
        """Exécute une action et retourne (next_state, reward, done)."""
        pass

    @abstractmethod
    def render(self):
        """Affiche le jeu (optionnel)."""
        pass

    @abstractmethod
    def get_state(self):
        """Retourne l'état du jeu sous forme de vecteur normalisé."""
        pass

    def to_tensor(self, game_state=None):
        """Convertit l'état actuel du jeu en tenseur."""
        state = self.get_state(game_state) if game_state else self.get_state()
        return np.array(state).reshape(-1)  # Génère automatiquement un tenseur


    @abstractmethod
    def get_available_actions(self):
        """Retourne la liste des actions disponibles dans l'environnement."""
        pass