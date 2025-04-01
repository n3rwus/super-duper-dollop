from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

"""
This module manages database connection and session handling.
"""

# Create SQLAlchemy engine
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get a database session
def get_db():
    """
    Dependency function to get a database session.
    
    Yields:
        SQLAlchemy session: Database session to execute queries
        
    Notes:
        Session is closed automatically after request is complete
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()