import numpy as np
from gym import spaces #type: ignore
from games.base_env import BaseGameEnv

class SnakeEnv(BaseGameEnv):
    """Environnement pour le jeu Snake."""
    
    def __init__(self, grid_size=10):
        super().__init__(grid_size)
        self.action_space = spaces.Discrete(4)
        self.reset()

    def reset(self):
        """Réinitialise le jeu et retourne l'état initial."""
        self.snake_pos = [self.grid_size // 2, self.grid_size // 2]
        self.snake_body = [self.snake_pos.copy()]
        self.food_pos = self._generate_food()
        self.done = False
        return self.get_state()

    def step(self, action):
        """Exécute une action et met à jour l'état du jeu."""
        if self.done:
            return self.get_state(), -10, True
        
        # Calcul de la distance avant le déplacement
        old_distance = abs(self.food_pos[0] - self.snake_pos[0]) + abs(self.food_pos[1] - self.snake_pos[1])

        new_head = self.snake_pos.copy()
        if action == 0: new_head[1] -= 1  # Haut
        if action == 1: new_head[1] += 1  # Bas
        if action == 2: new_head[0] -= 1  # Gauche
        if action == 3: new_head[0] += 1  # Droite

        if (new_head[0] < 0 or new_head[0] >= self.grid_size or
            new_head[1] < 0 or new_head[1] >= self.grid_size) :
            self.done = True
            return self.get_state(), -10, self.done  # Pénalité pour collision
        
        elif (new_head in self.snake_body[:-1]):
            self.done = True
            return self.get_state(), -10, self.done  # Pénalité pour collision
        
        # Calcul de la nouvelle distance
        new_distance = abs(self.food_pos[0] - self.snake_pos[0]) + abs(self.food_pos[1] - self.snake_pos[1])

        # Récompense basée sur la distance
        if new_distance < old_distance:
            distance_reward = 2  # Récompense pour se rapprocher
        elif new_distance > old_distance:
            distance_reward = -2  # Pénalité pour s'éloigner
        else:
            distance_reward = 0  # Pas de changement

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

    def get_state(self, game_state=None):
        """Retourne l'état du jeu sous forme de tuple."""
        if game_state:
            return tuple((
                game_state["snake"][0]["x"], 
                game_state["snake"][0]["y"], 
                game_state["food"]["x"], 
                game_state["food"]["y"]
            ))
        else:
            return tuple((
                int(self.snake_pos[0]), 
                int(self.snake_pos[1]), 
                int(self.food_pos[0]), 
                int(self.food_pos[1])
            ))


    
    def get_available_actions(self):
        """Retourne la liste des actions disponibles (haut, bas, gauche, droite)."""
        return ["UP", "DOWN", "LEFT", "RIGHT"]


    def _generate_food(self):
        """Génère la position de la nourriture."""
        while True:
            food_pos = np.random.randint(0, self.grid_size, size=2)
            if not any(np.array_equal(food_pos, pos) for pos in self.snake_body):
                return food_pos.tolist()

    def render(self):
        """Affichage minimal pour satisfaire la classe abstraite."""
        print(f"Snake: {self.snake_pos}, Food: {self.food_pos}, Done: {self.done}")

