"""Base player class."""
import numpy as np
from abc import ABC, abstractmethod
from datetime import datetime
from src.simulation.environment import Vector3, Aim, GameEnvironment


class BasePlayer(ABC):
    """Abstract base player."""
    
    def __init__(self, player_id: str, environment: GameEnvironment):
        self.player_id = player_id
        self.environment = environment
        self.position = environment.spawn_position()
        self.aim = Aim(yaw=0.0, pitch=0.0)
        self.velocity = Vector3(0, 0, 0)
        self.last_shot_time = None
        self.kills = 0
        self.deaths = 0
        self.headshots = 0
        
    @abstractmethod
    def update(self, dt: float) -> dict:
        """Update player state and return telemetry."""
        pass
    
    @abstractmethod
    def decide_action(self) -> str:
        """Decide next action (move, aim, shoot, etc.)."""
        pass
    
    def get_telemetry(self, action: str, **kwargs) -> dict:
        """Generate telemetry event."""
        return {
            "player_id": self.player_id,
            "timestamp": datetime.utcnow().timestamp(),
            "position": self.position.to_dict(),
            "aim": self.aim.to_dict(),
            "action": action,
            "velocity": self.velocity.to_dict(),
            **kwargs
        }