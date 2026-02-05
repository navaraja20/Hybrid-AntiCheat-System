"""Triggerbot player (auto-fire when crosshair on enemy)."""
import numpy as np
from datetime import datetime
from src.simulation.players.legit_player import LegitPlayer


class TriggerbotPlayer(LegitPlayer):
    """Player using triggerbot with timing jitter."""
    
    def __init__(self, player_id: str, environment, skill_level: float = 0.6):
        super().__init__(player_id, environment, skill_level)
        
        # Triggerbot characteristics
        self.base_click_interval = 0.12  # 120ms base
        self.click_jitter = 0.015  # 15ms jitter (still suspiciously low)
        
    def _shoot(self) -> dict:
        """Shoot with consistent timing."""
        now = datetime.utcnow().timestamp()
        
        # Suspiciously consistent click intervals
        if self.last_shot_time is not None:
            # Add small jitter to avoid perfect consistency
            expected_interval = self.base_click_interval + np.random.normal(0, self.click_jitter)
            time_since_last = now - self.last_shot_time
            
            if time_since_last < expected_interval:
                return self.get_telemetry("idle")
        
        self.last_shot_time = now
        
        # High accuracy due to automatic timing
        hit = np.random.random() < 0.85
        headshot = hit and (np.random.random() < self.headshot_probability)
        
        if hit:
            self.kills += (1 if np.random.random() < 0.4 else 0)
            if headshot:
                self.headshots += 1
        
        return self.get_telemetry(
            "fire",
            target_hit=hit,
            headshot=headshot,
            reaction_time=0.05  # Suspiciously fast
        )