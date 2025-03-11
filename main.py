from fastapi import FastAPI, WebSocket, BackgroundTasks # type: ignore
from pydantic import BaseModel # type: ignore
import sys
from importlib import import_module
import asyncio
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.settings import get_game_config, get_agent_config, get_model_path
from backend.models.model_manager import BaseModelManager

app = FastAPI()

# ✅ Variables globales pour gérer l'état du training/inférence
training_task = None
inference_task = None
pause_training = False
pause_inference = False

# ✅ Modèle Pydantic pour valider l'état du jeu
class GameState(BaseModel):
    snake: list[dict]
    food: dict
    score: int

# ✅ Lancer l'entraînement
@app.post("/training/start")
async def start_training(background_tasks: BackgroundTasks):
    global training_task, pause_training
    if training_task and not training_task.done():
        return {"status": "Training already running"}
    
    pause_training = False
    training_task = asyncio.create_task(train_model())
    return {"status": "Training started"}

# ✅ Arrêter l'entraînement
@app.post("/training/stop")
async def stop_training():
    global training_task
    if training_task:
        training_task.cancel()
        training_task = None
        return {"status": "Training stopped"}
    return {"status": "No training is running"}

# ✅ Mettre en pause l'entraînement
@app.post("/training/pause")
async def pause_training_func():
    global pause_training
    pause_training = True
    return {"status": "Training paused"}

# ✅ Lancer l'inférence
@app.post("/inference/start")
async def start_inference(background_tasks: BackgroundTasks):
    global inference_task, pause_inference
    if inference_task and not inference_task.done():
        return {"status": "Inference already running"}
    
    pause_inference = False
    inference_task = asyncio.create_task(run_inference())
    return {"status": "Inference started"}

# ✅ Arrêter l'inférence
@app.post("/inference/stop")
async def stop_inference():
    global inference_task
    if inference_task:
        inference_task.cancel()
        inference_task = None
        return {"status": "Inference stopped"}
    return {"status": "No inference is running"}

# ✅ Mettre en pause l'inférence
@app.post("/inference/pause")
async def pause_inference_func():
    global pause_inference
    pause_inference = True
    return {"status": "Inference paused"}

# ✅ WebSocket : Communication en temps réel
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        game_state = await websocket.receive_json()
        action = handle_game_state(game_state)
        await websocket.send_json(action)

# ✅ Fonction pour gérer l'état du jeu
def handle_game_state(game_state):
    # Génère une réponse d'action en fonction de l'état du jeu
    state = game_state["state"]
    action = {"direction": "UP"}  # Exemple simple
    return action

# ✅ Fonction d'entraînement
async def train_model():
    global pause_training
    agent_config = get_agent_config()
    game_config = get_game_config()

    # Charger le modèle et l'agent
    env_module = import_module(game_config["module"])
    env_class = getattr(env_module, game_config["class"])
    env = env_class()

    agent_module = import_module(agent_config["module"])
    agent_class = getattr(agent_module, agent_config["class"])
    agent = agent_class(env)

    model_path = get_model_path(agent_config["version_agent"].lower())
    manager_class = BaseModelManager.get_manager_class(agent_config["version_agent"].lower())
    model_manager = manager_class()

    if os.path.exists(model_path):
        model = model_manager.load_model(model_path)
        agent.set_model(model)

    # 🔁 Boucle d'entraînement
    num_episodes = agent_config.get("num_episodes", 10000)
    for episode in range(num_episodes):
        if pause_training:
            await asyncio.sleep(1)
            continue

        state = env.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            state, reward, done = env.step(action)

        print(f"Episode {episode + 1} terminé")

    # ✅ Sauvegarder le modèle
    model_manager.save_model(agent.get_model(), model_path)

# ✅ Fonction d'inférence
async def run_inference():
    global pause_inference
    agent_config = get_agent_config()
    game_config = get_game_config()

    # Charger le modèle et l'agent
    env_module = import_module(game_config["module"])
    env_class = getattr(env_module, game_config["class"])
    env = env_class()

    agent_module = import_module(agent_config["module"])
    agent_class = getattr(agent_module, agent_config["class"])
    agent = agent_class(env)

    model_path = get_model_path(agent_config["version_agent"].lower())
    manager_class = BaseModelManager.get_manager_class(agent_config["version_agent"].lower())
    model_manager = manager_class()

    if os.path.exists(model_path):
        model = model_manager.load_model(model_path)
        agent.set_model(model)

    # 🔁 Boucle d'inférence
    for episode in range(10):
        if pause_inference:
            await asyncio.sleep(1)
            continue

        state = env.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            state, reward, done = env.step(action)

        print(f"Inference {episode + 1} terminé")

# ✅ Démarrage du serveur
if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=7000)
