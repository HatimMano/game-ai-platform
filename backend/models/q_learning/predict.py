import os
import json
import logging
import numpy as np
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from agents.q_learning.q_learning_agent import QLearningAgent
from games.snake.snake_env import SnakeEnv
from models.model_manager import BaseModelManager
from config.settings import get_model_path, get_params, DATA_DIR


# Configuration des logs
log_path = os.path.join(DATA_DIR, "q_learning", "log.txt")
logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(message)s")

# Charger les hyperparamètres depuis params.json
params = get_params("q_learning")

# Charger l'environnement
env = SnakeEnv()

# Initialiser l'agent avec les hyperparamètres chargés
agent = QLearningAgent(env,version="q_learning")


# Charger le modèle entraîné
model_path = get_model_path("q_learning")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Le modèle {model_path} est introuvable. Lance d'abord train.py.")

agent.Q_table = BaseModelManager.load_model(model_path)

# Exécuter une partie de test
num_episodes = 10  # Définir le nombre d'épisodes de test
all_predictions = []


print(f"Début du test sur {num_episodes} épisodes...")

for episode in range(num_episodes):
    print('Episode : ' + str(episode))
    state = tuple(env.reset())
    done = False
    total_reward = 0
    episode_data = {"episode": episode + 1, "steps": []}
    max_steps = 500
    step_count = 0


    while not done and step_count < max_steps:
        step_count += 1
        action = np.argmax(agent.Q_table[tuple(state)]) # Sélectionner la meilleure action selon la Q-table
        state, reward, done = env.step(action)
        total_reward += reward
        #env.render()  # afficher l'évolution du jeu
        # Sauvegarder l'action et la récompense
        episode_data["steps"].append({
            "state": str(state),
            "action": int(action),
            "reward": reward
        })

    episode_data["final_score"] = total_reward
    all_predictions.append(episode_data)

    # Log de la performance de l'agent
    logging.info(f"Épisode {episode + 1} - Score : {total_reward}")

# Sauvegarde des prédictions dans /data/q_learning/predictions.json
predictions_path = os.path.join(DATA_DIR, "q_learning", "predictions.json")

with open(predictions_path, "w") as f:
    json.dump(all_predictions, f, indent=4)

print(f"Test terminé. Prédictions sauvegardées dans {predictions_path}")
