import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from games.snake.snake_env import SnakeEnv
from agents.q_learning.q_learning_agent import QLearningAgent
import pickle
from starlette.websockets import WebSocketState, WebSocketDisconnect


app = FastAPI()

# CORS (pour permettre le front React de se connecter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = SnakeEnv(grid_size=10)
agent = QLearningAgent(env)

# Variables de contrôle
training_active = False
inference_active = False
inference_task = None


# Démarrage du training
@app.post("/start-training")
async def start_training(episodes: int = 1000):
    global training_active
    if training_active:
        return {"status": "Training already in progress"}
    
    training_active = True
    agent.train(episodes)
    training_active = False
    return {"status": "Training finished"}

# Sauvegarde du modèle
@app.post("/save-model")
async def save_model():
    model_path = os.path.join("backend", "models", "q_learning", "model.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(agent.get_model(), f)
    return {"status": "Model saved"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global inference_active, inference_task
    await websocket.accept()
    print("Connexion WebSocket établie")

    try:
        data = await websocket.receive_json()
        if data.get("action") == "start":
            inference_active = True
            state = tuple(env.reset())
            print("Envoie du state initial")
            print(state)

            try:
                if websocket.client_state == WebSocketState.CONNECTED:
                    print('✅ WebSocket est encore connecté')
                    await websocket.send_json({"state": state, "done": False})
            except Exception as e:
                print(f"❌ Erreur lors de l'envoi initial : {e}")

            # ✅ Fonction keep_alive définie dans le contexte local
            async def keep_alive():
                while inference_active and websocket.client_state == WebSocketState.CONNECTED:
                    await asyncio.sleep(1)

            async def run_inference(initial_state):
                global inference_active
                try:
                    state = initial_state
                    print("🚀 Début de la boucle d'inférence")

                    while inference_active and websocket.client_state == WebSocketState.CONNECTED:
                        print("🔄 Boucle en cours...")
                        action = agent.choose_action(state)
                        next_state, reward, done = env.step(action)

                        if websocket.client_state == WebSocketState.CONNECTED:
                            await websocket.send_json({
                                "state": next_state,
                                "reward": reward,
                                "done": done
                            })

                        state = next_state
                        if done:
                            state = tuple(env.reset())
                            await asyncio.sleep(1)

                except Exception as e:
                    print(f"❌ Erreur dans run_inference : {e}")
                finally:
                    inference_active = False
                    print("🏁 Fin de la boucle d'inférence")

            # ✅ Crée la boucle d'inférence
            if inference_task is None or inference_task.done():
                inference_task = asyncio.create_task(run_inference(state))
                print(f"🚀 Tâche lancée : {inference_task}")

                # ✅ Lance la boucle keep_alive directement dans le contexte
                asyncio.create_task(keep_alive())

                # ✅ Force FastAPI à garder le contexte ouvert
                await asyncio.sleep(3600)

    except WebSocketDisconnect:
        print("❌ Connexion WebSocket fermée par le client")
        inference_active = False
    except Exception as e:
        print(f"❌ WebSocket Error: {e}")
    finally:
        inference_active = False
        if inference_task is not None:
            inference_task.cancel()
            inference_task = None
            print(f"🚫 Tâche annulée → État du WebSocket : {websocket.client_state}")

@app.post("/stop-inference")
async def stop_inference():
    global inference_active, inference_task
    print("🛑 Réception de la commande STOP")
    inference_active = False
    if inference_task is not None:
        inference_task.cancel()
        inference_task = None
    return {"status": "Inference stopped"}
