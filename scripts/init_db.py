"""Initialize database schema."""
from src.database.postgres import init_db
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def main():
    """Run database initialization."""
    logger.info("Initializing database schema...")
    
    try:
        init_db()
        logger.info("Database initialized successfully!")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    main()