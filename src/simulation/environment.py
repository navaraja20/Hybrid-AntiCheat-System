"""Game environment simulation."""
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Vector3:
    """3D vector."""
    x: float
    y: float
    z: float
    
    def distance_to(self, other: 'Vector3') -> float:
        """Calculate Euclidean distance."""
        return np.sqrt(
            (self.x - other.x)**2 + 
            (self.y - other.y)**2 + 
            (self.z - other.z)**2
        )
    
    def to_dict(self):
        return {"x": self.x, "y": self.y, "z": self.z}


@dataclass
class Aim:
    """Aim direction (spherical coordinates)."""
    yaw: float  # Horizontal angle (-180 to 180)
    pitch: float  # Vertical angle (-90 to 90)
    
    def to_dict(self):
        return {"yaw": self.yaw, "pitch": self.pitch}


class GameEnvironment:
    """Simulated game environment."""
    
    def __init__(self, map_size: Tuple[float, float, float] = (1000, 1000, 100)):
        self.map_size = map_size
        self.players = []
        
    def spawn_position(self) -> Vector3:
        """Generate random spawn position."""
        return Vector3(
            x=np.random.uniform(0, self.map_size[0]),
            y=np.random.uniform(0, self.map_size[1]),
            z=0.0  # Ground level
        )
    
    def get_nearby_players(self, position: Vector3, radius: float = 100) -> list:
        """Get players within radius."""
        nearby = []
        for player in self.players:
            if position.distance_to(player.position) <= radius:
                nearby.append(player)
        return nearby