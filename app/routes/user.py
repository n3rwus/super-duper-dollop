from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import UserCreate, Token
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

router = APIRouter(tags=["Authentication"])

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Args:
        user_data (UserCreate): User registration data with email and password
        db (Session): Database session
        
    Returns:
        Token: Access token for the new user
        
    Raises:
        HTTPException: If the email is already registered
    """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    try:
        token = user_service.register_user(user_data.email, user_data.password)
        return token
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Authenticate a user and return an access token.
    
    Args:
        user_data (UserCreate): User login data with email and password
        db (Session): Database session
        
    Returns:
        Token: Access token upon successful login
        
    Raises:
        HTTPException: If the credentials are invalid
    """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    token = user_service.authenticate_user(user_data.email, user_data.password)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return token