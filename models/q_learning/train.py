import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import json
from agents.q_learning.q_learning_agent import QLearningAgent
from games.snake.snake_env import SnakeEnv
from models.model_manager import BaseModelManager
from config.settings import get_params, get_model_path

# Charger les hyperparamètres depuis params.json
params = get_params("q_learning")


# Charger l'environnement de jeu
env = SnakeEnv()

# Initialiser l'agent avec les hyperparamètres chargés
agent = QLearningAgent(env,version="q_learning")

# Définir le nombre d'épisodes d'entraînement
num_episodes = params["num_episodes"]

print(f"Lancement de l'entraînement du modèle (q_learning) sur {num_episodes} épisodes...")

# Lancer l'entraînement
agent.train(num_episodes)

# Sauvegarde du modèle entraîné
model_path = get_model_path("q_learning")  # Utilisation de settings.py pour récupérer le chemin du modèle

BaseModelManager.save_model(agent.Q_table, model_path)

print(f"Modèle entraîné et sauvegardé dans {model_path}")
