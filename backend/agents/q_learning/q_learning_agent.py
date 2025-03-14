import os
import sys
import numpy as np
import random
import pickle
import pandas as pd # type: ignore
from collections import defaultdict
from config.settings import get_params, DATA_DIR
import asyncio



# Ajouter le dossier racine `Snake_V3/` au PYTHONPATH pour éviter ModuleNotFoundError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Imports après l'ajout du PYTHONPATH
from agents.base_agent import BaseAgent



class QLearningAgent(BaseAgent):
    """Agent basé sur le Q-Learning."""

    def __init__(self, env, version="q_learning"):
        super().__init__(env)
        self.Q_table = {}
        
        # Charger les hyperparamètres depuis `settings.py`
        params = get_params(version)
        
        self.alpha = params["alpha"]  
        self.gamma = params["gamma"]  
        self.epsilon = params["epsilon"]  
        self.epsilon_inference = params["epsilon_inference"]  
        self.epsilon_min = params["epsilon_min"]  
        self.epsilon_decay = params["epsilon_decay"]  
        self.Q_table = defaultdict(self.default_q_values)

        # ✅ Variables d'état
        self.current_episode = 0
        self.current_state = None
        self.training_active = False
    
    def default_q_values(self):
        """Retourne un tableau de zéros correspondant au nombre d'actions possibles."""
        return np.zeros(self.env.action_space.n)

    def choose_action(self, state, inference=False):
        """Sélectionne une action selon une stratégie epsilon-greedy."""
        epsilon = self.epsilon_inference if inference else self.epsilon
        if random.uniform(0, 1) < epsilon:
            return self.env.action_space.sample()  # Exploration
        if state not in self.Q_table:
            self.Q_table[state] = np.zeros(self.env.action_space.n)
        return np.argmax(self.Q_table[tuple(state)])  # Exploitation

    async def train(self, num_episodes):
        """Entraîne l'agent sur un certain nombre d'épisodes."""
        print("🚀 Training started...")
        self.training_active = True

        # ✅ Reprendre l'état précédent s'il existe
        episode = self.current_episode if self.current_episode else 0
        state = self.current_state if self.current_state else tuple(self.env.reset())
        
        while self.training_active and episode < num_episodes:
            done = False
            total_reward = 0

            while not done and self.training_active:
                print("first" + str(done))
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                print("2nd" + str(done))
                next_state = tuple(next_state)

                if next_state not in self.Q_table:
                    self.Q_table[next_state] = np.zeros(self.env.action_space.n)

                best_next_action = np.argmax(self.Q_table[next_state])
                td_target = reward + self.gamma * self.Q_table[next_state][best_next_action]
                self.Q_table[state][action] += self.alpha * (td_target - self.Q_table[state][action])

                state = next_state
                total_reward += reward

                # ✅ Ajout d'un délai pour éviter une surcharge CPU
                await asyncio.sleep(0.01)

            # ✅ Enregistrement de la progression
            self.current_episode = episode
            self.current_state = state

            # Mise à jour de l'exploration
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

            print(f"✅ Épisode {episode} terminé - Reward: {total_reward}")

            episode += 1
        
        print("🏁 Training stopped")

    def stop_training(self):
        """Arrête complètement l'entraînement."""
        self.training_active = False
        self.current_episode = 0
        self.current_state = None
        print("🛑 Training reset")

    def get_model(self):
        """Retourne la table Q pour la sauvegarde."""
        return self.Q_table

    def set_model(self, model):
        """Définit la table Q après chargement."""
        self.Q_table = model

    def load_model(self, model_path=None):
        if model_path is None:
            model_path = os.path.join("models", "q_learning", "model.pkl")
        
        if os.path.exists(model_path):
            print(f"📥 Chargement du modèle depuis {model_path}...")
            with open(model_path, "rb") as f:
                self.Q_table = pickle.load(f)
            print(f"✅ Modèle chargé → Taille Q-table : {len(self.Q_table)}")
            sample_keys = list(self.Q_table.keys())[:5]
            for key in sample_keys:
                print(f"État : {key} → Valeurs Q : {self.Q_table[key]}")
        else:
            print("⚠️ Aucun modèle trouvé → Initialisation d'un modèle vide")
            self.Q_table = defaultdict(self.default_q_values)
