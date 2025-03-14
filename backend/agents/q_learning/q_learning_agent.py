import os
import sys
import numpy as np
import random
import pickle
from collections import defaultdict
from config.settings import get_params
import asyncio

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.base_agent import BaseAgent

class QLearningAgent(BaseAgent):
    """Q-Learning based agent."""

    def __init__(self, env, version="q_learning"):
        super().__init__(env)
        self.Q_table = defaultdict(self.default_q_values)

        # Load hyperparameters from settings
        params = get_params(version)
        self.alpha = params["alpha"]
        self.gamma = params["gamma"]
        self.epsilon = params["epsilon"]
        self.epsilon_inference = params["epsilon_inference"]
        self.epsilon_min = params["epsilon_min"]
        self.epsilon_decay = params["epsilon_decay"]

        # State variables
        self.current_episode = 0
        self.current_state = None
        self.training_active = False

    def default_q_values(self):
        """Return a zero-filled array matching action space size."""
        return np.zeros(self.env.action_space.n)

    def choose_action(self, state, inference=False):
        """Select an action using an epsilon-greedy policy."""
        epsilon = self.epsilon_inference if inference else self.epsilon
        if random.uniform(0, 1) < epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.Q_table[tuple(state)])

    async def train(self, num_episodes):
        """Train the agent over a number of episodes."""
        self.training_active = True
        episode = self.current_episode or 0
        state = self.current_state or tuple(self.env.reset())

        while self.training_active and episode < num_episodes:
            done = False
            total_reward = 0

            while not done and self.training_active:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                next_state = tuple(next_state)

                if next_state not in self.Q_table:
                    self.Q_table[next_state] = np.zeros(self.env.action_space.n)

                best_next_action = np.argmax(self.Q_table[next_state])
                td_target = reward + self.gamma * self.Q_table[next_state][best_next_action]
                self.Q_table[state][action] += self.alpha * (td_target - self.Q_table[state][action])

                state = next_state
                total_reward += reward

                await asyncio.sleep(0.01)

            self.current_episode = episode
            self.current_state = state
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

            episode += 1

    def stop_training(self):
        self.training_active = False
        self.current_episode = 0
        self.current_state = None

    def get_model(self):
        return self.Q_table

    def set_model(self, model):
        self.Q_table = model

    def load_model(self, model_path=None):
        if model_path is None:
            model_path = os.path.join("models", "q_learning", "model.pkl")

        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                self.Q_table = pickle.load(f)

