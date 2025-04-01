from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.models import User
from app.core.security import get_password_hash, verify_password

class UserRepository:
    """
    Repository class for User-related database operations.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.
        
        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email address.
        
        Args:
            email (str): Email address to search for
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by ID.
        
        Args:
            user_id (int): User ID to search for
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, email: str, password: str) -> User:
        """
        Create a new user with the given email and password.
        
        Args:
            email (str): User's email address
            password (str): User's password (will be hashed)
            
        Returns:
            User: The created user object
        """
        hashed_password = get_password_hash(password)
        user = User(email=email, password=hashed_password)
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            email (str): User's email address
            password (str): User's password
            
        Returns:
            Optional[User]: User object if authentication is successful, None otherwise
        """
        user = self.get_user_by_email(email)
        
        if not user:
            return None
            
        if not verify_password(password, user.password):
            return None
            
        return user