from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Optional

from app.core.security import decode_access_token
from app.db.database import get_db
from app.repositories.user_repository import UserRepository
from app.models.models import User

"""
This module handles authentication-related functionality including token validation
and user identification.
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from a token.
    
    Args:
        token (str): JWT token from the request
        db (Session): Database session
        
    Returns:
        User: The authenticated user
        
    Raises:
        HTTPException: If the token is invalid or the user doesn't exist
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    
    try:
        payload = decode_access_token(token)
        user_id: Optional[int] = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
        
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id)
    
    if user is None:
        raise credentials_exception
        
    return user
