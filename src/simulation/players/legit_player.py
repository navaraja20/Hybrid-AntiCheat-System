"""Legitimate player simulation."""
import numpy as np
from datetime import datetime
from src.simulation.players.base_player import BasePlayer


class LegitPlayer(BasePlayer):
    """Simulates realistic human player behavior."""
    
    def __init__(self, player_id: str, environment, skill_level: float = 0.5):
        super().__init__(player_id, environment)
        self.skill_level = np.clip(skill_level, 0.1, 0.9)  # 0.1=noob, 0.9=pro
        
        # Human characteristics
        self.reaction_time = 0.2 + (0.3 * (1 - self.skill_level))  # 0.2-0.5s
        self.aim_smoothness = 5 + (10 * (1 - self.skill_level))  # Lower = smoother
        self.headshot_probability = 0.1 + (0.4 * self.skill_level)  # 10-50%
        
    def update(self, dt: float) -> dict:
        """Update player state."""
        action = self.decide_action()
        
        if action == "move":
            return self._move(dt)
        elif action == "aim":
            return self._aim(dt)
        elif action == "shoot":
            return self._shoot()
        else:
            return self.get_telemetry("idle")
    
    def decide_action(self) -> str:
        """Randomly decide action."""
        actions = ["move", "aim", "shoot", "idle"]
        weights = [0.4, 0.3, 0.2, 0.1]
        return np.random.choice(actions, p=weights)
    
    def _move(self, dt: float) -> dict:
        """Simulate movement."""
        # Random direction with some momentum
        direction = np.random.uniform(-np.pi, np.pi)
        speed = np.random.uniform(3, 7)  # units/second
        
        # Update position with smooth acceleration
        self.velocity.x += np.cos(direction) * speed * dt * 0.1
        self.velocity.y += np.sin(direction) * speed * dt * 0.1
        
        # Damping (friction)
        self.velocity.x *= 0.9
        self.velocity.y *= 0.9
        
        # Update position
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        
        # Clamp to map bounds
        self.position.x = np.clip(self.position.x, 0, self.environment.map_size[0])
        self.position.y = np.clip(self.position.y, 0, self.environment.map_size[1])
        
        return self.get_telemetry("move", speed=speed)
    
    def _aim(self, dt: float) -> dict:
        """Simulate human aiming."""
        # Add small random adjustments (human micro-corrections)
        aim_delta_yaw = np.random.normal(0, self.aim_smoothness)
        aim_delta_pitch = np.random.normal(0, self.aim_smoothness * 0.5)
        
        self.aim.yaw += aim_delta_yaw * dt
        self.aim.pitch += aim_delta_pitch * dt
        
        # Clamp pitch
        self.aim.pitch = np.clip(self.aim.pitch, -89, 89)
        
        # Wrap yaw
        if self.aim.yaw > 180:
            self.aim.yaw -= 360
        elif self.aim.yaw < -180:
            self.aim.yaw += 360
        
        return self.get_telemetry("aim")
    
    def _shoot(self) -> dict:
        """Simulate shooting."""
        now = datetime.utcnow().timestamp()
        
        # Human click interval variability
        if self.last_shot_time is not None:
            time_since_last = now - self.last_shot_time
            if time_since_last < 0.1:  # Too fast, skip
                return self.get_telemetry("idle")
        
        self.last_shot_time = now
        
        # Determine hit/headshot based on skill
        hit = np.random.random() < (0.3 + 0.5 * self.skill_level)
        headshot = hit and (np.random.random() < self.headshot_probability)
        
        if hit:
            self.kills += (1 if np.random.random() < 0.3 else 0)
            if headshot:
                self.headshots += 1
        
        return self.get_telemetry(
            "fire",
            target_hit=hit,
            headshot=headshot,
            reaction_time=self.reaction_time
        )