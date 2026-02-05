"""Main game simulation client."""
import time
import json
from typing import List
from kafka import KafkaProducer
from src.simulation.environment import GameEnvironment
from src.simulation.players.legit_player import LegitPlayer
from src.simulation.players.aimbot_player import AimbotPlayer
from src.simulation.players.triggerbot_player import TriggerbotPlayer
from src.simulation.players.wallhack_player import WallhackPlayer
from src.utils.config import get_settings
from src.utils.logging import setup_logger

logger = setup_logger(__name__)
settings = get_settings()


class GameSimulator:
    """Game simulation orchestrator."""
    
    def __init__(self, num_legit: int = 80, num_aimbot: int = 5, 
                 num_triggerbot: int = 5, num_wallhack: int = 10):
        self.environment = GameEnvironment()
        self.players = []
        self.tick_rate = 60  # 60 FPS
        self.dt = 1.0 / self.tick_rate
        
        # Create Kafka producer
        self.producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Spawn players
        self._spawn_players(num_legit, num_aimbot, num_triggerbot, num_wallhack)
        
    def _spawn_players(self, num_legit, num_aimbot, num_triggerbot, num_wallhack):
        """Create player instances."""
        player_id = 0
        
        # Legit players
        for i in range(num_legit):
            skill = np.random.uniform(0.2, 0.8)
            player = LegitPlayer(f"player_{player_id:04d}", self.environment, skill)
            self.players.append(player)
            self.environment.players.append(player)
            player_id += 1
        
        # Aimbot players
        for i in range(num_aimbot):
            smoothness = np.random.uniform(0.7, 0.9)
            player = AimbotPlayer(f"player_{player_id:04d}", self.environment, smoothness)
            self.players.append(player)
            self.environment.players.append(player)
            player_id += 1
        
        # Triggerbot players
        for i in range(num_triggerbot):
            player = TriggerbotPlayer(f"player_{player_id:04d}", self.environment)
            self.players.append(player)
            self.environment.players.append(player)
            player_id += 1
        
        # Wallhack players
        for i in range(num_wallhack):
            player = WallhackPlayer(f"player_{player_id:04d}", self.environment)
            self.players.append(player)
            self.environment.players.append(player)
            player_id += 1
        
        logger.info(f"Spawned {len(self.players)} players")
    
    def run(self, duration_seconds: int = 300):
        """Run simulation for specified duration."""
        logger.info(f"Starting simulation for {duration_seconds}s...")
        
        start_time = time.time()
        tick_count = 0
        
        while time.time() - start_time < duration_seconds:
            tick_start = time.time()
            
            # Update all players
            for player in self.players:
                telemetry = player.update(self.dt)
                
                # Send to Kafka
                self.producer.send(
                    settings.kafka_topic_telemetry,
                    value=telemetry
                )
            
            tick_count += 1
            
            # Log progress every 60 ticks (1 second)
            if tick_count % 60 == 0:
                logger.info(f"Tick {tick_count} | Players: {len(self.players)}")
            
            # Sleep to maintain tick rate
            elapsed = time.time() - tick_start
            sleep_time = max(0, self.dt - elapsed)
            time.sleep(sleep_time)
        
        logger.info(f"Simulation complete: {tick_count} ticks")
        self.producer.flush()
        self.producer.close()


def main():
    """Main entry point."""
    simulator = GameSimulator(
        num_legit=80,
        num_aimbot=5,
        num_triggerbot=5,
        num_wallhack=10
    )
    simulator.run(duration_seconds=300)


if __name__ == "__main__":
    import numpy as np  # Import here for random in spawning
    main()