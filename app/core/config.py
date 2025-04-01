# app/core/config.py
from pydantic_settings import BaseSettings  # Changed from pydantic.BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    
    Attributes:
        APP_NAME (str): Name of the application
        DB_USER (str): Database username
        DB_PASSWORD (str): Database password
        DB_HOST (str): Database host address
        DB_NAME (str): Database name
        SECRET_KEY (str): Secret key for token generation and validation
        ALGORITHM (str): Algorithm used for JWT encoding/decoding
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Token expiration time in minutes
    """
    APP_NAME: str = "SocialAPI"
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "social_api")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"


settings = Settings()