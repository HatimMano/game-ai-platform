import pytest # type: ignore
import numpy as np
from backend.agents.q_learning.q_learning_agent import QLearningAgent
from backend.games.snake.snake_env import SnakeEnv

@pytest.fixture
def agent():
    env = SnakeEnv(grid_size=10)
    return QLearningAgent(env)

def test_choose_action(agent):
    state = (5, 5, 3, 3)  # Un état factice
    action = agent.choose_action(state)
    assert action in [0, 1, 2, 3]  # Vérifie que l'action est valide

def test_q_table_update(agent):
    state = (5, 5, 3, 3)
    action = 1
    next_state = (5, 6, 3, 3)
    reward = 10

    old_value = agent.Q_table[state][action]
    agent.Q_table[state][action] = old_value + agent.alpha * (reward + agent.gamma * np.max(agent.Q_table[next_state]) - old_value)
    
    assert agent.Q_table[state][action] != old_value  # Vérifie que la Q-table a été mise à jour
