import os
import sys
import numpy as np
import random
import pickle
import pandas as pd # type: ignore
from collections import defaultdict
from config.settings import get_params, DATA_DIR


# Ajouter le dossier racine `Snake_V3/` au PYTHONPATH pour éviter ModuleNotFoundError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Imports après l'ajout du PYTHONPATH
from agents.base_agent import BaseAgent

def default_q_values(action_space_size):
    """Retourne un tableau de zéros correspondant au nombre d'actions possibles."""
    return np.zeros(action_space_size)


class QLearningAgent(BaseAgent):
    """Agent basé sur le Q-Learning."""

    def __init__(self, env, version="q_learning"):
        super().__init__(env)
        self.Q_table = {}
        
        # Charger les hyperparamètres depuis `settings.py`
        params = get_params(version)  # Récupère les params de v1, v2...
        
        self.alpha = params["alpha"]  
        self.gamma = params["gamma"]  
        self.epsilon = params["epsilon"]  
        self.epsilon_min = params["epsilon_min"]  
        self.epsilon_decay = params["epsilon_decay"]  
        self.Q_table = defaultdict(lambda: np.zeros(env.action_space.n))


    def choose_action(self, state, epsilon=None):
        """Sélectionne une action selon une stratégie epsilon-greedy."""
        epsilon = epsilon if epsilon is not None else self.epsilon
        if random.uniform(0, 1) < epsilon:
            return self.env.action_space.sample()  # Exploration
        if state not in self.Q_table:
                self.Q_table[state] = np.zeros(self.env.action_space.n)
        return np.argmax(self.Q_table[tuple(state)])  # Exploitation
    


    def train(self, num_episodes, version="q_learning"):
        """Entraîne l'agent sur un certain nombre d'épisodes."""
        scores = []  # Liste des scores
        
        for episode in range(num_episodes):
            state = tuple(self.env.reset())
            done = False
            total_reward = 0

            while not done:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                next_state = tuple(next_state)
                
                if next_state not in self.Q_table:
                    self.Q_table[next_state] = np.zeros(self.env.action_space.n)

                best_next_action = np.argmax(self.Q_table[next_state])
                td_target = reward + self.gamma * self.Q_table[next_state][best_next_action]
                self.Q_table[state][action] += self.alpha * (td_target - self.Q_table[state][action])

                state = next_state
                total_reward += reward

            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            scores.append((episode, total_reward))  # Stocke l’épisode et le score
        
        # Sauvegarde des scores dans `/data/v1/training_scores.csv`
        scores_path = os.path.join(DATA_DIR, version, "training_scores.csv")
        os.makedirs(os.path.dirname(scores_path), exist_ok=True)  # Crée le dossier s'il n'existe pas
        df = pd.DataFrame(scores, columns=["episode", "score"])
        df.to_csv(scores_path, index=False)

        print(f"Scores sauvegardés dans {scores_path}")


    def get_model(self):
        """Retourne la table Q pour la sauvegarde."""
        return self.Q_table

    def set_model(self, model):
        """Définit la table Q après chargement."""
        self.Q_table = model