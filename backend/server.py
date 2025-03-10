import json
import os
import sys
import webbrowser
from importlib import import_module
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import numpy as np
from config.settings import get_server_config, get_model_path, get_game_config, get_agent_config
from models.model_manager import BaseModelManager

# Ajout du chemin du projet pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Initialisation de FastAPI
app = FastAPI()

# Modèle Pydantic pour valider les données reçues via WebSocket
class GameState(BaseModel):
    state: dict  # L'état du jeu sous forme de dictionnaire

class ActionResponse(BaseModel):
    direction: str  # La réponse de l'agent sous forme de direction

def open_game():
    """Ouvre automatiquement index.html dans le navigateur."""
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/index.html"))
    webbrowser.open(f"file://{frontend_path}")

class GameServer:
    """Serveur pour gérer les connexions avec le client, adaptable à plusieurs jeux et modèles IA."""

    def __init__(self):
        # Récupération des configurations serveur
        server_config = get_server_config()
        self.host = server_config["host"]
        self.port = server_config["port"]

        # Chargement de l'environnement de jeu
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
        manager_class = BaseModelManager.get_manager_class(agent_config["version_agent"].lower())
        model_manager = manager_class()
        model = model_manager.load_model(model_path)
        self.agent.set_model(model)

    async def handle_websocket_connection(self, websocket: WebSocket):
        """Gère la communication WebSocket entre le client (frontend) et l'IA."""
        await websocket.accept()
        async for message in websocket:
            # Reçoit l'état du jeu et le valide avec Pydantic
            game_state = GameState(**json.loads(message))

            # Extraction de l'état de manière générique
            state = self.env.to_tensor(game_state.state)

            # Choix de l'action par l'agent
            action = self.agent.choose_action(state)

            # Envoi de l'action au client
            actions = self.env.get_available_actions()
            action_response = ActionResponse(direction=actions[action])
            await websocket.send_json(action_response.dict())

# Initialisation du serveur
server = GameServer()

# Endpoint WebSocket pour la communication en temps réel
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await server.handle_websocket_connection(websocket)

# Endpoint HTTP pour ouvrir le jeu
@app.get("/open-game")
def open_game_endpoint():
    open_game()
    return {"message": "Jeu ouvert dans le navigateur."}

# Endpoint HTTP pour obtenir la configuration du serveur
@app.get("/server-config")
def get_server_config_endpoint():
    return get_server_config()

# Point d'entrée pour exécuter le serveur
if __name__ == "__main__":
    import uvicorn
    open_game()
    uvicorn.run(app, host=server.host, port=server.port)