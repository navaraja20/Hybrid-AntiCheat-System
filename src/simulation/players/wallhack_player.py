"""Wallhack/ESP player (knows enemy positions)."""
import numpy as np
from src.simulation.players.legit_player import LegitPlayer
from src.simulation.environment import Vector3


class WallhackPlayer(LegitPlayer):
    """Player using ESP/wallhack."""
    
    def __init__(self, player_id: str, environment, skill_level: float = 0.7):
        super().__init__(player_id, environment, skill_level)
        
    def _move(self, dt: float) -> dict:
        """Move with knowledge of enemy positions (low path entropy)."""
        # Simulate moving toward enemies (too efficient navigation)
        # In real game, this would be detected by path entropy
        
        # Generate "optimal" path (straight line to objectives)
        target_x = np.random.uniform(0, self.environment.map_size[0])
        target_y = np.random.uniform(0, self.environment.map_size[1])
        
        # Move directly toward target (low entropy)
        dx = target_x - self.position.x
        dy = target_y - self.position.y
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance > 1:
            # Normalized direction
            dx /= distance
            dy /= distance
            
            speed = 5.0
            self.position.x += dx * speed * dt
            self.position.y += dy * speed * dt
        
        self.position.x = np.clip(self.position.x, 0, self.environment.map_size[0])
        self.position.y = np.clip(self.position.y, 0, self.environment.map_size[1])
        
        return self.get_telemetry("move", speed=5.0, path_type="optimal")