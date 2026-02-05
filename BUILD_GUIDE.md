# 🛠️ Step-by-Step Build Guide: Anti-Cheat System

**Complete Implementation Guide from Zero to Production**

This guide will walk you through building the entire anti-cheat system from scratch. Follow each step sequentially, and by the end, you'll have a fully functional production-ready system.

**Estimated Time**: 40-60 hours  
**Difficulty**: Intermediate to Advanced  
**Prerequisites**: Python knowledge, basic ML understanding, Docker familiarity, Anaconda/Miniconda installed

---

## 📋 Table of Contents

1. [Environment Setup](#phase-1-environment-setup)
2. [Project Foundation](#phase-2-project-foundation)
3. [Database & Infrastructure](#phase-3-database--infrastructure)
4. [Game Simulation](#phase-4-game-simulation)
5. [Telemetry Collection](#phase-5-telemetry-collection)
6. [Feature Engineering](#phase-6-feature-engineering)
7. [Rule-Based Detection](#phase-7-rule-based-detection)
8. [ML Models - Anomaly Detection](#phase-8-anomaly-detection)
9. [ML Models - Supervised Learning](#phase-9-supervised-learning)
10. [Decision Engine](#phase-10-decision-engine)
11. [Review Queue & Feedback](#phase-11-review-queue--feedback)
12. [Monitoring & Dashboards](#phase-12-monitoring--dashboards)
13. [Testing & Validation](#phase-13-testing--validation)
14. [Deployment](#phase-14-deployment)
15. [Final Evaluation](#phase-15-final-evaluation)

---

# Phase 1: Environment Setup

**Duration**: 1-2 hours  
**Goal**: Get your development environment ready

## Step 1.1: Install Core Tools

### Windows
```powershell
# Install Anaconda or Miniconda
# Anaconda (full): https://www.anaconda.com/download
# Miniconda (minimal): https://docs.conda.io/en/latest/miniconda.html

# Install Docker Desktop
# Download: https://www.docker.com/products/docker-desktop

# Install Git
# Download: https://git-scm.com/downloads

# Verify installations (open new terminal after installing conda)
conda --version
python --version  # Should be 3.9+
docker --version
git --version
```

### Linux/Mac
```bash
# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# Follow prompts, then restart terminal

# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Git
sudo apt-get install git

# Verify
conda --version
python --version
docker --version
git --version
```

## Step 1.2: Create Project Directory

```bash
# Create project root
mkdir anti-cheat-system
cd anti-cheat-system

# Initialize git
git init
```

## Step 1.3: Set Up Conda Environment

```bash
# Create conda environment
conda create -n anticheat python=3.9 -y

# Activate (Windows/Linux/Mac)
conda activate anticheat

# You should see (anticheat) in your terminal prompt

# Verify Python version
python --version
```

## Step 1.4: Create Initial Requirements File

Create `requirements.txt`:
```txt
# API & Web
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Data Processing
pandas==2.1.3
numpy==1.26.2
scipy==1.11.4

# Machine Learning
scikit-learn==1.3.2
xgboost==2.0.2
torch==2.1.1
joblib==1.3.2

# Streaming & Messaging
kafka-python==2.0.2
redis==5.0.1

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
influxdb-client==1.38.0

# Monitoring
prometheus-client==0.19.0
grafana-client==3.7.0

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
python-multipart==0.0.6

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
httpx==0.25.2

# Development
black==23.12.0
mypy==1.7.1
pre-commit==3.6.0
ipython==8.18.1
jupyter==1.0.0
```

Install dependencies:
```bash
# Make sure conda environment is activated
conda activate anticheat

# Install packages
pip install -r requirements.txt
```

## Step 1.5: Verify Installation

```bash
# Test imports
python -c "import fastapi, pandas, sklearn, torch; print('✅ All packages installed!')"

# (Optional) Export environment for reproducibility
conda env export > environment.yml
```

**✅ Checkpoint**: You should have Python, Docker, conda environment activated, and all packages installed without errors.

---

# Phase 2: Project Foundation

**Duration**: 2-3 hours  
**Goal**: Set up project structure and configuration

## Step 2.1: Create Directory Structure

### Windows (PowerShell)
```powershell
# Create all directories
New-Item -ItemType Directory -Force -Path src/api, src/simulation, src/processing, src/detection, src/review, src/training, src/database, src/utils
New-Item -ItemType Directory -Force -Path src/api/routes
New-Item -ItemType Directory -Force -Path src/simulation/players
New-Item -ItemType Directory -Force -Path src/processing/features
New-Item -ItemType Directory -Force -Path src/detection/models
New-Item -ItemType Directory -Force -Path tests/unit, tests/integration, tests/adversarial
New-Item -ItemType Directory -Force -Path configs
New-Item -ItemType Directory -Force -Path scripts
New-Item -ItemType Directory -Force -Path docker
New-Item -ItemType Directory -Force -Path grafana/dashboards
New-Item -ItemType Directory -Force -Path notebooks
New-Item -ItemType Directory -Force -Path data/telemetry, data/models, data/logs
```

### Linux/Mac (Bash)
```bash
# Create all directories
mkdir -p src/{api,simulation,processing,detection,review,training,database,utils}
mkdir -p src/api/routes
mkdir -p src/simulation/players
mkdir -p src/processing/features
mkdir -p src/detection/models
mkdir -p tests/{unit,integration,adversarial}
mkdir -p configs
mkdir -p scripts
mkdir -p docker
mkdir -p grafana/dashboards
mkdir -p notebooks
mkdir -p data/{telemetry,models,logs}
```

## Step 2.2: Create Configuration Files

### `.env` file:
```env
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=anticheat
POSTGRES_USER=admin
POSTGRES_PASSWORD=changeme123

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_TELEMETRY=game.telemetry

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# InfluxDB
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=my-super-secret-token
INFLUXDB_ORG=anticheat
INFLUXDB_BUCKET=telemetry

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Detection Thresholds
THRESHOLD_IMMEDIATE_BAN=0.95
THRESHOLD_SHADOW_BAN=0.85
THRESHOLD_REVIEW_QUEUE=0.70

# Model Paths
MODEL_PATH_ISOLATION_FOREST=data/models/isolation_forest.pkl
MODEL_PATH_XGBOOST=data/models/xgboost.pkl
MODEL_PATH_AUTOENCODER=data/models/autoencoder.pth
```

### `configs/feature_config.yaml`:
```yaml
features:
  jerk:
    enabled: true
    threshold: 1000
    window_size: 10
    
  click_interval:
    enabled: true
    cv_threshold: 0.1
    min_samples: 20
    
  path_entropy:
    enabled: true
    entropy_threshold: 2.5
    bin_size: 45
    
  headshot_rate:
    enabled: true
    rate_threshold: 0.8
    reaction_time_threshold: 0.1
    
  recoil_compensation:
    enabled: true
    variance_threshold: 0.05

temporal:
  windows:
    - 30
    - 300
    - 1800
```

## Step 2.3: Create Utility Modules

### `src/utils/config.py`:
```python
"""Configuration management."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "anticheat"
    postgres_user: str = "admin"
    postgres_password: str = "changeme123"
    
    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic_telemetry: str = "game.telemetry"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    
    # Detection Thresholds
    threshold_immediate_ban: float = 0.95
    threshold_shadow_ban: float = 0.85
    threshold_review_queue: float = 0.70
    
    # Model Paths
    model_path_isolation_forest: str = "data/models/isolation_forest.pkl"
    model_path_xgboost: str = "data/models/xgboost.pkl"
    model_path_autoencoder: str = "data/models/autoencoder.pth"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

### `src/utils/logging.py`:
```python
"""Structured logging configuration."""
import logging
import sys
from datetime import datetime


def setup_logger(name: str) -> logging.Logger:
    """Create a configured logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger
```

### `src/__init__.py`:
```python
"""Anti-cheat system package."""
__version__ = "1.0.0"
```

Create empty `__init__.py` in all subdirectories:
```bash
# Linux/Mac
find src -type d -exec touch {}/__init__.py \;

# Windows (PowerShell)
Get-ChildItem -Path src -Recurse -Directory | ForEach-Object { New-Item -Path "$($_.FullName)\__init__.py" -ItemType File -Force }
```

**✅ Checkpoint**: You should have a structured project with configs and utility modules.

---

# Phase 3: Database & Infrastructure

**Duration**: 2-3 hours  
**Goal**: Set up databases and message queue

## Step 3.1: Create Docker Compose Configuration

### `docker-compose.yml`:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: anticheat-postgres
    environment:
      POSTGRES_DB: anticheat
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: changeme123
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: anticheat-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    container_name: anticheat-zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    container_name: anticheat-kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
    healthcheck:
      test: ["CMD", "kafka-broker-api-versions", "--bootstrap-server", "localhost:9092"]
      interval: 10s
      timeout: 10s
      retries: 5

  influxdb:
    image: influxdb:2.7-alpine
    container_name: anticheat-influxdb
    ports:
      - "8086:8086"
    environment:
      DOCKER_INFLUXDB_INIT_MODE: setup
      DOCKER_INFLUXDB_INIT_USERNAME: admin
      DOCKER_INFLUXDB_INIT_PASSWORD: changeme123
      DOCKER_INFLUXDB_INIT_ORG: anticheat
      DOCKER_INFLUXDB_INIT_BUCKET: telemetry
      DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: my-super-secret-token
    volumes:
      - influxdb-data:/var/lib/influxdb2

  grafana:
    image: grafana/grafana:10.2.2
    container_name: anticheat-grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin
      GF_INSTALL_PLUGINS: grafana-clock-panel
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    depends_on:
      - influxdb

volumes:
  postgres-data:
  redis-data:
  influxdb-data:
  grafana-data:
```

## Step 3.2: Start Infrastructure

```bash
# Start all services
docker-compose up -d

# Verify all services are running
docker-compose ps

# Check logs if any service failed
docker-compose logs <service-name>

# Wait for services to be healthy (may take 1-2 minutes)
```

## Step 3.3: Create Database Models

### `src/database/models.py`:
```python
"""SQLAlchemy ORM models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Player(Base):
    """Player information."""
    __tablename__ = "players"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_sessions = Column(Integer, default=0)
    total_playtime = Column(Float, default=0.0)
    status = Column(String, default="clean")  # clean, flagged, banned, shadow_banned
    

class DetectionEvent(Base):
    """Detection events for audit trail."""
    __tablename__ = "detection_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    event_type = Column(String, nullable=False)  # rule_violation, anomaly, ban, etc.
    severity = Column(Float)
    features = Column(JSON)
    details = Column(JSON)
    

class Ban(Base):
    """Ban records."""
    __tablename__ = "bans"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(String, nullable=False, index=True)
    banned_at = Column(DateTime, default=datetime.utcnow)
    ban_type = Column(String, nullable=False)  # permanent, shadow, temporary
    reason = Column(String)
    evidence = Column(JSON)
    confidence_score = Column(Float)
    reviewed = Column(Boolean, default=False)
    appeal_status = Column(String, default=None)  # None, pending, approved, rejected


class ReviewCase(Base):
    """Cases pending human review."""
    __tablename__ = "review_cases"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(Integer, default=0)  # Higher = more urgent
    status = Column(String, default="pending")  # pending, reviewed, escalated
    cheat_score = Column(Float)
    features = Column(JSON)
    reviewer_id = Column(String, default=None)
    verdict = Column(String, default=None)  # clean, ban, shadow_ban
    reviewed_at = Column(DateTime, default=None)
    notes = Column(String, default=None)
```

### `src/database/postgres.py`:
```python
"""PostgreSQL connection manager."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from src.utils.config import get_settings
from src.database.models import Base

settings = get_settings()

# Database URL
DATABASE_URL = (
    f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    

@contextmanager
def get_db() -> Session:
    """Get database session context manager."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

## Step 3.4: Initialize Database

### `scripts/init_db.py`:
```python
"""Initialize database schema."""
from src.database.postgres import init_db
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def main():
    """Run database initialization."""
    logger.info("Initializing database schema...")
    
    try:
        init_db()
        logger.info("✅ Database initialized successfully!")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    main()
```

Run initialization:
```bash
python scripts/init_db.py
```

**✅ Checkpoint**: All infrastructure services running, database schema created.

---

# Phase 4: Game Simulation

**Duration**: 4-6 hours  
**Goal**: Create realistic player behavior simulation

## Step 4.1: Create Base Player Classes

### `src/simulation/environment.py`:
```python
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
```

### `src/simulation/players/base_player.py`:
```python
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
```

## Step 4.2: Implement Legitimate Player

### `src/simulation/players/legit_player.py`:
```python
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
```

## Step 4.3: Implement Cheat Players

### `src/simulation/players/aimbot_player.py`:
```python
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
```

### `src/simulation/players/triggerbot_player.py`:
```python
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
```

### `src/simulation/players/wallhack_player.py`:
```python
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
```

## Step 4.4: Create Game Client Simulator

### `src/simulation/game_client.py`:
```python
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
```

**✅ Checkpoint**: You can now run the game simulator and generate telemetry data.

Test it:
```bash
python src/simulation/game_client.py
```

You should see Kafka messages being produced.

---

# Phase 5: Telemetry Collection

**Duration**: 2-3 hours  
**Goal**: Build FastAPI service to collect telemetry

## Step 5.1: Create API Models

### `src/api/models.py`:
```python
"""Pydantic models for API."""
from pydantic import BaseModel, Field
from typing import Optional


class Vector3Model(BaseModel):
    x: float
    y: float
    z: float


class AimModel(BaseModel):
    yaw: float = Field(..., ge=-180, le=180)
    pitch: float = Field(..., ge=-90, le=90)


class TelemetryEvent(BaseModel):
    player_id: str
    timestamp: float
    position: Vector3Model
    aim: AimModel
    action: str
    velocity: Optional[Vector3Model] = None
    target_hit: Optional[bool] = None
    headshot: Optional[bool] = None
    reaction_time: Optional[float] = None
    speed: Optional[float] = None


class PlayerStatusResponse(BaseModel):
    player_id: str
    cheat_score: float
    status: str
    last_updated: str
```

## Step 5.2: Create API Routes

### `src/api/routes/telemetry.py`:
```python
"""Telemetry ingestion routes."""
from fastapi import APIRouter, HTTPException
from kafka import KafkaProducer
import json
from src.api.models import TelemetryEvent
from src.utils.config import get_settings
from src.utils.logging import setup_logger

router = APIRouter()
logger = setup_logger(__name__)
settings = get_settings()

# Kafka producer (singleton)
producer = None


def get_producer():
    """Get or create Kafka producer."""
    global producer
    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    return producer


@router.post("/telemetry")
async def ingest_telemetry(event: TelemetryEvent):
    """Ingest telemetry event."""
    try:
        # Send to Kafka
        kafka_producer = get_producer()
        kafka_producer.send(
            settings.kafka_topic_telemetry,
            value=event.model_dump()
        )
        
        return {"status": "accepted", "player_id": event.player_id}
    
    except Exception as e:
        logger.error(f"Failed to ingest telemetry: {e}")
        raise HTTPException(status_code=500, detail="Ingestion failed")


@router.get("/player/{player_id}/status")
async def get_player_status(player_id: str):
    """Get player cheat detection status."""
    # TODO: Query from database/cache
    return {
        "player_id": player_id,
        "cheat_score": 0.0,
        "status": "clean",
        "last_updated": "2026-02-03T12:00:00Z"
    }
```

## Step 5.3: Create Main API Application

### `src/api/collector.py`:
```python
"""FastAPI telemetry collector service."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import telemetry
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Anti-Cheat Telemetry Collector",
    description="Ingests game telemetry for cheat detection",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(telemetry.router, prefix="/api/v1", tags=["telemetry"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "telemetry-collector"}


@app.on_event("startup")
async def startup_event():
    """Startup tasks."""
    logger.info("🚀 Telemetry collector starting...")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown tasks."""
    logger.info("👋 Telemetry collector shutting down...")


if __name__ == "__main__":
    import uvicorn
    from src.utils.config import get_settings
    
    settings = get_settings()
    uvicorn.run(
        "src.api.collector:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
```

**✅ Checkpoint**: API server can receive and forward telemetry to Kafka.

Test it:
```bash
# Terminal 1: Start API
python src/api/collector.py

# Terminal 2: Test endpoint
curl http://localhost:8000/health

# Visit API docs
# http://localhost:8000/docs
```

---

**Continue to Part 2 of the guide for Phases 6-15...**

This guide continues with:
- Phase 6: Feature Engineering
- Phase 7: Rule-Based Detection
- Phase 8: Anomaly Detection
- Phase 9: Supervised Learning
- Phase 10: Decision Engine
- Phase 11: Review Queue
- Phase 12: Monitoring
- Phase 13: Testing
- Phase 14: Deployment
- Phase 15: Final Evaluation

Would you like me to continue with the remaining phases in a follow-up file (BUILD_GUIDE_PART2.md)?
