
import numpy as np
from gym import spaces # type: ignore
from games.base_env import BaseGameEnv

class SnakeEnv(BaseGameEnv):
    """Environment for the Snake game."""
    
    def __init__(self, grid_size=10):
        super().__init__(grid_size)
        self.action_space = spaces.Discrete(4)
        self.reset()

    def reset(self):
        """Reset the game and return the initial state."""
        self.snake_pos = [self.grid_size // 2, self.grid_size // 2]
        self.snake_body = [self.snake_pos.copy()]
        self.food_pos = self._generate_food()
        self.done = False
        return self.get_state()

    def step(self, action):
        """Execute an action and update the game state."""
        if self.done:
            return self.get_state(), -10, True
        
        # Distance before moving
        old_distance = abs(self.food_pos[0] - self.snake_pos[0]) + abs(self.food_pos[1] - self.snake_pos[1])

        # Update snake position based on action
        new_head = self.snake_pos.copy()
        if action == 0:
            new_head[1] -= 1  # Up
        elif action == 1:
            new_head[1] += 1  # Down
        elif action == 2:
            new_head[0] -= 1  # Left
        elif action == 3:
            new_head[0] += 1  # Right

        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= self.grid_size or
            new_head[1] < 0 or new_head[1] >= self.grid_size or
            new_head in self.snake_body[:-1]):
            self.done = True
            return self.get_state(), -10, self.done

        # Distance after moving
        new_distance = abs(self.food_pos[0] - new_head[0]) + abs(self.food_pos[1] - new_head[1])

        # Distance-based reward
        distance_reward = 2 if new_distance < old_distance else -2 if new_distance > old_distance else 0

        self.snake_body.insert(0, new_head)
        self.snake_pos = new_head

        reward = -0.01
        if new_head == self.food_pos:
            reward = 10 + distance_reward
            self.food_pos = self._generate_food()
        else:
            reward = distance_reward
            self.snake_body.pop()

        return self.get_state(), reward, self.done

    def get_state(self):
        """Return the current game state as a tuple."""
        return (self.snake_pos[0], self.snake_pos[1], self.food_pos[0], self.food_pos[1])

    def get_available_actions(self):
        """Return a list of available actions (up, down, left, right)."""
        return ["UP", "DOWN", "LEFT", "RIGHT"]

    def _generate_food(self):
        """Generate food at a random position that is not occupied by the snake."""
        while True:
            food_pos = np.random.randint(0, self.grid_size, size=2).tolist()
            if food_pos not in self.snake_body:
                return food_pos

    def render(self):
        """Minimal console display for debugging purposes."""
        print(f"Snake: {self.snake_pos}, Food: {self.food_pos}, Done: {self.done}")
