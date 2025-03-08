import asyncio
import websockets #type: ignore
import json
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import webbrowser
from importlib import import_module
from config.settings import get_server_config, get_model_path, get_game_config, get_agent_config, AGENT_CONFIG
from models.model_manager import BaseModelManager



def open_game():
    """Ouvre automatiquement index.html dans le navigateur."""
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/index.html"))
    webbrowser.open(f"file://{frontend_path}")


class GameServer:
    """Serveur WebSocket pour gérer les connexions avec le client, adaptable à plusieurs jeux et modèles IA."""

    def __init__(self):
        # Récupération des configurations serveur
        server_config = get_server_config()
        self.host = server_config["host"]
        self.port = server_config["port"]

        # Chargement l'environnement de jeu
        game_config = get_game_config()
        env_module = import_module(game_config["module"])
        env_class = getattr(env_module, game_config["class"])
        self.env = env_class()

        # Chargement de l'agent
        agent_config = get_agent_config()
        agent_module = import_module(agent_config["module"])
        agent_class = getattr(agent_module, agent_config["class"])
        self.agent = agent_class(self.env)

        # Chargement du modèle IA
        model_path = get_model_path(agent_config["version_agent"].lower())
        self.agent.load_model(model_path)  

    async def handle_connection(self, websocket):
        """Gère la communication entre le client (frontend) et l'IA."""
        async for message in websocket:
            game_state = json.loads(message)

            # Extraction de l'état de manière générique
            state = self.env.to_tensor(game_state)

            # Choix de l'action par l'agent
            action = self.agent.choose_action(state)

            # Envoi de l'action au client
            actions = self.env.get_available_actions()
            action_response = {"direction": actions[action]}
            await websocket.send(json.dumps(action_response))

    async def start_server(self):
        """Démarre le serveur WebSocket."""
        async with websockets.serve(self.handle_connection, self.host, self.port):
            await asyncio.Future()  # Run forever


if __name__ == "__main__":
    server = GameServer()
    open_game()
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("Serveur arrêté par l'utilisateur.")




def real_time_learning(action,state,self):
    # Exécuter l'action dans l'environnement et récupérer le nouvel état
    next_state, reward, done = self.env.step(action)

    # Met à jour la Q-table
    state_tuple = tuple(state)
    next_state_tuple = tuple(next_state)

    best_next_action = np.argmax(self.agent.Q_table[next_state_tuple])
    td_target = reward + self.agent.gamma * self.agent.Q_table[next_state_tuple][best_next_action]
    td_error = td_target - self.agent.Q_table[state_tuple][action]
    self.agent.Q_table[state_tuple][action] += self.agent.alpha * td_error

    # Sauvegarde la Q-table après chaque mort du serpent
    if done:
        BaseModelManager.save_model(self.agent.Q_table)
        print(" Partie terminée, Q-table sauvegardée.")