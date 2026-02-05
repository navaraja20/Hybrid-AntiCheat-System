"""Aimbot player simulation (realistic, not naive)."""
import numpy as np
from datetime import datetime
from src.simulation.players.base_player import BasePlayer


class AimbotPlayer(BasePlayer):
    """Simulates a player using smooth aimbot."""
    
    def __init__(self, player_id: str, environment, smoothness: float = 0.8):
        super().__init__(player_id, environment)
        self.smoothness = smoothness  # 0=instant snap, 1=very smooth
        self.fov_limit = 45  # Only lock within 45° cone
        self.reaction_delay = 0.15  # Fake human reaction time
        self.accuracy = 0.98  # 98% hit rate (not 100% to avoid detection)
        self.headshot_rate = 0.85  # 85% headshots
        
    def update(self, dt: float) -> dict:
        """Update with aimbot logic."""
        action = self.decide_action()
        
        if action == "aim" or action == "shoot":
            return self._aimbot_assist(dt, shoot=(action == "shoot"))
        else:
            # Normal movement to blend in
            return self._move_normal(dt)
    
    def decide_action(self) -> str:
        """Aimbot players shoot more often."""
        actions = ["aim", "shoot", "move"]
        weights = [0.4, 0.4, 0.2]
        return np.random.choice(actions, p=weights)
    
    def _aimbot_assist(self, dt: float, shoot: bool = False) -> dict:
        """Smooth aimbot with realistic constraints."""
        # Find nearest enemy (simulated)
        target_yaw = np.random.uniform(-180, 180)
        target_pitch = np.random.uniform(-30, 30)
        
        # Calculate angle difference
        yaw_diff = target_yaw - self.aim.yaw
        pitch_diff = target_pitch - self.aim.pitch
        
        # Normalize angle difference
        if yaw_diff > 180:
            yaw_diff -= 360
        elif yaw_diff < -180:
            yaw_diff += 360
        
        # Only assist if within FOV
        angle_distance = np.sqrt(yaw_diff**2 + pitch_diff**2)
        
        if angle_distance < self.fov_limit:
            # Smooth approach (not instant snap!)
            smooth_factor = (1 - self.smoothness) * 50 * dt
            self.aim.yaw += yaw_diff * smooth_factor
            self.aim.pitch += pitch_diff * smooth_factor
            
            # Clamp
            self.aim.pitch = np.clip(self.aim.pitch, -89, 89)
        else:
            # Normal human-like aim adjustment
            self.aim.yaw += np.random.normal(0, 2) * dt
            self.aim.pitch += np.random.normal(0, 1) * dt
        
        if shoot:
            return self._shoot_with_aimbot()
        else:
            return self.get_telemetry("aim")
    
    def _shoot_with_aimbot(self) -> dict:
        """Shoot with aimbot accuracy."""
        now = datetime.utcnow().timestamp()
        
        # Still add slight variance to click timing
        if self.last_shot_time is not None:
            time_since_last = now - self.last_shot_time
            if time_since_last < 0.08:
                return self.get_telemetry("idle")
        
        self.last_shot_time = now
        
        # High accuracy but not 100%
        hit = np.random.random() < self.accuracy
        headshot = hit and (np.random.random() < self.headshot_rate)
        
        if hit:
            self.kills += 1
            if headshot:
                self.headshots += 1
        
        return self.get_telemetry(
            "fire",
            target_hit=hit,
            headshot=headshot,
            reaction_time=self.reaction_delay
        )
    
    def _move_normal(self, dt: float) -> dict:
        """Normal movement to blend in."""
        direction = np.random.uniform(-np.pi, np.pi)
        speed = np.random.uniform(4, 6)
        
        self.position.x += np.cos(direction) * speed * dt
        self.position.y += np.sin(direction) * speed * dt
        
        self.position.x = np.clip(self.position.x, 0, self.environment.map_size[0])
        self.position.y = np.clip(self.position.y, 0, self.environment.map_size[1])
        
        return self.get_telemetry("move", speed=speed)