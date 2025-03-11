import os
import json

#Définition des chemins vers les principaux dossiers du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "backend", "models")
DATA_DIR = os.path.join(BASE_DIR, "backend", "data")
LOGS_DIR = os.path.join(BASE_DIR, "backend", "logs")


#Versions de modèles disponibles
AVAILABLE_MODELS = ["q_learning", "dqn"]

#Configuration des logs
LOGGING_CONFIG = {
    "log_file": os.path.join(LOGS_DIR, "training.log"),
    "log_level": "INFO",
}

#Paramètres généraux de l'agent (valables pour toutes les versions)
GENERAL_CONFIG = {
    "max_steps_per_episode": 500,  # Nombre maximum d'actions avant timeout
    "render": False,  # Activer/désactiver l'affichage de l'environnement
    "save_frequency": 1000,  # Sauvegarde automatique tous les X épisodes
}

#Configuration du serveur
SERVER_CONFIG = {
    "host": "localhost",
    "port": 8000,
    "use_websocket": True,   # True → utilise WebSocket, False → utilise HTTP uniquement
}


GAME_CONFIG = {
    "selected_game": "snake",
    "games": {
        "snake": {"module": "backend.games.snake.snake_env", "class": "SnakeEnv"},
        "chess": {"module": "backend.games.chess.chess_env", "class": "ChessEnv"}
    }
}

AGENT_CONFIG = {
    "selected_agent": "q_learning",
    "agents": {
        "q_learning": {"module": "backend.agents.q_learning.q_learning_agent",
                       "class": "QLearningAgent",
                       "version_agent": "q_learning"
        },
        "dqn": {"module": "backend.agents.dqn.dqn_agent",
                "class": "DQNAgent",
                "version_agent": "dqn"
        }
    }
}




def get_params(version):
    """Charge et retourne les hyperparamètres d'une version donnée."""
    params_path = os.path.join(MODELS_DIR, version, "params.json")
    
    if not os.path.exists(params_path):
        raise FileNotFoundError(f"Le fichier {params_path} est introuvable.")

    with open(params_path, "r") as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Impossible de lire {params_path}. Vérifie son format JSON.")

    return params  # Retourne directement les hyperparamètres sous forme de dictionnaire


#Fonction utilitaire pour obtenir le chemin du modèle sauvegardé
def get_model_path(agent_name):
    return os.path.join(MODELS_DIR, str(agent_name), "model.pkl")





def get_server_config():
    """Retourne la configuration du serveur."""
    return {
        "host": "localhost",
        "port": 8000
    }

def get_game_config():
    """Récupère la configuration du jeu sélectionné."""
    game_key = GAME_CONFIG["selected_game"]
    return GAME_CONFIG["games"].get(game_key, {})


def get_agent_config():
    """Récupère la configuration de l’agent sélectionné."""
    agent_key = AGENT_CONFIG["selected_agent"]
    return AGENT_CONFIG["agents"].get(agent_key, {})