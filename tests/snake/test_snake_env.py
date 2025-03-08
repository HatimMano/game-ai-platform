import pytest # type: ignore
import numpy as np
from games.snake.snake_env import SnakeEnv

@pytest.fixture
def env():
    return SnakeEnv(grid_size=10)

def test_reset(env):
    state = env.reset()
    assert isinstance(state, np.ndarray)
    assert len(state) == 4  # [snake_x, snake_y, food_x, food_y]

def test_step(env):
    state = env.reset()
    action = 0  # Mouvement vers le haut
    new_state, reward, done = env.step(action)

    assert isinstance(new_state, np.ndarray)
    assert isinstance(reward, float)
    assert isinstance(done, bool)

def test_collision_wall(env):
    env.reset()
    env.snake_pos = [0, 0]  # Place le Snake dans un coin
    new_state, reward, done = env.step(2)  # Essaye d'aller à gauche (hors de la grille)
    assert done is True
    assert reward == -50  # Vérifie la pénalité
