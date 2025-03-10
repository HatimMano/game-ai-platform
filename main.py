import argparse
import asyncio
from importlib import import_module
from config.settings import AGENT_CONFIG, get_game_config, get_agent_config, get_model_path
from models.model_manager import BaseModelManager
import os
import webbrowser
import sys


def train():
    agent_config = get_agent_config()
    
    # Import dynamique de l'agent
    agent_module = import_module(agent_config["module"])
    agent_class = getattr(agent_module, agent_config["class"])

    game_config = get_game_config()
    env_module = import_module(game_config["module"])
    env_class = getattr(env_module, game_config["class"])

    # Créer l'environnement et l'agent
    env = env_class()
    agent = agent_class(env)

    # Charger les hyperparamètres
    manager_class = BaseModelManager.get_manager_class(agent_config["version_agent"].lower())
    model_manager = manager_class()
    model_path = get_model_path(agent_config["version_agent"].lower())

    if os.path.exists(model_path):
        print(f"Chargement du modèle depuis : {model_path}")
        model = model_manager.load_model(model_path)
        agent.set_model(model)
    else:
        print("Aucun modèle existant. Initialisation d'un nouvel agent.")

    # Lancer l'entraînement
    num_episodes = agent_config.get("num_episodes", 10000)
    print(f"Lancement de l'entraînement sur {num_episodes} épisodes...")
    agent.train(num_episodes)

    # Sauvegarde après entraînement
    model_manager.save_model(agent.get_model(), model_path)
    print(f"Modèle sauvegardé dans : {model_path}")

def test():
    agent_config = get_agent_config()

    # Import dynamique de l'agent
    agent_module = import_module(agent_config["module"])
    agent_class = getattr(agent_module, agent_config["class"])

    game_config = get_game_config()
    env_module = import_module(game_config["module"])
    env_class = getattr(env_module, game_config["class"])

    # Créer l'environnement et l'agent
    env = env_class()
    agent = agent_class(env)
    # Charger le modèle entraîné
    agent_config = get_agent_config()
    model_path = get_model_path(agent_config["version_agent"].lower())
    manager_class = BaseModelManager.get_manager_class(agent_config["version_agent"].lower())
    model_manager = manager_class()
    if os.path.exists(model_path):
        print(f"Chargement du modèle depuis : {model_path}")
        model = model_manager.load_model(model_path)
        agent.set_model(model)
    else:
        print(model_path)
        print("Modèle introuvable. Lance d'abord l'entraînement.")
        return

    num_episodes = 10
    print(f"Lancement du test sur {num_episodes} épisodes...")

    total_score = 0
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        episode_score = 0

        while not done:
            action = agent.choose_action(state)
            state, reward, done = env.step(action)
            episode_score += reward
        
        total_score += episode_score
        print(f"Épisode {episode + 1} - Score : {episode_score}")

    print(f"Score moyen : {total_score / num_episodes:.2f}")

async def start_server():
    from backend.server import GameServer

    print("Lancement du serveur...")
    server = GameServer()
    await server.start_server()

def main():
    parser = argparse.ArgumentParser(description="AI Game Platform")
    
    # Définition des arguments disponibles
    parser.add_argument("--train", action="store_true", help="Lancer l'entraînement")
    parser.add_argument("--test", action="store_true", help="Lancer le test")
    parser.add_argument("--serve", action="store_true", help="Démarrer le serveur WebSocket")

    args = parser.parse_args()

    if args.train:
        train()

    if args.test:
        test()

    if args.serve:
        try:
            asyncio.run(start_server())
        except KeyboardInterrupt:
            print("Serveur arrêté par l'utilisateur.")
        

if __name__ == "__main__":
    main()
