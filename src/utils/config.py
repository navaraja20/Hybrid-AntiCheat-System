from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "anticheat"
    postgres_user: str = "admin"
    postgres_password: str = "admin"
    
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