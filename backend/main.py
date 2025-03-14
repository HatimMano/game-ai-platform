
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from games.snake.snake_env import SnakeEnv
from agents.q_learning.q_learning_agent import QLearningAgent
import pickle
from starlette.websockets import WebSocketState # type: ignore

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize environment and agent
env = SnakeEnv(grid_size=10)
agent = QLearningAgent(env)

# Control variables
training_active = False
inference_active = False
inference_task = None

@app.post("/start-training")
async def start_training(episodes: int = 1000):
    """Start the training loop."""
    global training_active
    if training_active:
        return {"status": "Training already in progress"}

    training_active = True
    agent.training_active = True
    asyncio.create_task(agent.train(episodes))
    return {"status": "Training started"}

@app.post("/stop-training")
async def stop_training():
    """Stop the training loop."""
    global training_active
    if not training_active:
        return {"status": "No training in progress"}

    training_active = False
    agent.stop_training()
    return {"status": "Training stopped"}

@app.post("/save-model")
async def save_model():
    """Save the Q-learning model to file."""
    global training_active
    if training_active:
        return {"status": "Cannot save model during training"}

    model_path = os.path.join("models", "q_learning", "model.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(agent.get_model(), f)

    return {"status": "Model saved"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connection for inference."""
    global inference_active, inference_task
    await websocket.accept()

    try:
        data = await websocket.receive_json()

        if data.get("action") == "start":
            inference_active = True
            state = tuple(env.reset())
            await websocket.send_json({"state": state, "done": False})

            async def run_inference(initial_state):
                global inference_active
                state = initial_state

                while inference_active and websocket.client_state == WebSocketState.CONNECTED:
                    action = agent.choose_action(state)
                    next_state, reward, done = env.step(action)
                    await websocket.send_json({"state": next_state, "reward": reward, "done": done})
                    state = next_state

                    if done:
                        state = tuple(env.reset())

            if inference_task is None or inference_task.done():
                inference_task = asyncio.create_task(run_inference(state))
                await asyncio.sleep(3600)

        elif data.get("action") == "pause":
            inference_active = False
            if inference_task is not None:
                inference_task.cancel()
                inference_task = None

    except WebSocketDisconnect:
        inference_active = False

@app.post("/stop-inference")
async def stop_inference():
    """Stop the inference loop."""
    global inference_active, inference_task
    inference_active = False
    if inference_task is not None:
        inference_task.cancel()
        inference_task = None
    return {"status": "Inference stopped"}
