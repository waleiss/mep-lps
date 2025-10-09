# Database Configuration - PostgreSQL connection for users
# Implements RNF2.1 for password encryption
# Uses clean configuration management

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=settings.debug  # Enable SQL logging in debug mode
)

# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables
    """
    from models import Base
    Base.metadata.create_all(bind=engine)