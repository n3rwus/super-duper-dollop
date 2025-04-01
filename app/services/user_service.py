from typing import Optional, Dict
from datetime import timedelta
from app.repositories.user_repository import UserRepository
from app.core.security import create_access_token
from app.core.config import settings
from app.schemas.schemas import Token

class UserService:
    """
    Service class for user-related business logic.
    """
    
    def __init__(self, user_repository: UserRepository):
        """
        Initialize the service with a user repository.
        
        Args:
            user_repository (UserRepository): Repository for user database operations
        """
        self.user_repository = user_repository
    
    def register_user(self, email: str, password: str) -> Token:
        """
        Register a new user and generate an access token.
        
        Args:
            email (str): User's email address
            password (str): User's password
            
        Returns:
            Token: Access token for the new user
            
        Raises:
            ValueError: If the email is already registered
        """
        # Check if user already exists
        existing_user = self.user_repository.get_user_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create new user
        user = self.user_repository.create_user(email, password)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    def authenticate_user(self, email: str, password: str) -> Optional[Token]:
        """
        Authenticate a user and generate an access token.
        
        Args:
            email (str): User's email address
            password (str): User's password
            
        Returns:
            Optional[Token]: Access token if authentication is successful, None otherwise
        """
        user = self.user_repository.authenticate_user(email, password)
        
        if not user:
            return None
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return Token(access_token=access_token, token_type="bearer")