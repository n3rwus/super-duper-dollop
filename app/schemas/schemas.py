from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    """
    Base Pydantic model for user data validation.
    
    Attributes:
        email (EmailStr): User's email address with email format validation
    """
    email: EmailStr = Field(..., description="User's email address")
     
    
class UserCreate(UserBase):
    """
    Pydantic model for user creation with password validation.
    
    Attributes:
        password (str): User's password with length validation
    """
    password: str = Field(..., min_length=8, max_length=100, description="User's passwords")
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # Add more password strength validations as needed
        return v


class UserResponse(UserBase):
    """
    Pydantic model for user response data.
    
    Attributes:
        id (int): User's ID
        created_at (datetime): Timestamp when the user was created
    """
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
class Token(BaseModel):
    """
    Pydantic model for token response.
    
    Attributes:
        access_token (str): JWT or generated token string
        token_type (str): Type of token, typically "bearer"
    """
    access_token: str
    token_type: str = "bearer"
    
    
class PostBase(BaseModel):
    """
    Base Pydantic model for post data validation.
    
    Attributes:
        text (str): Content of the post with length validation
    """
    text: str = Field(..., min_length=1, max_length=1000000, description="Post content")
    
    @validator('text')
    def check_payload_size(cls, v):
        """Validate that post payload is under 1MB."""
        # Rough estimate: 1 character = 1 byte
        if len(v.encode('utf-8')) > 1024 * 1024:  # 1 MB
            raise ValueError('Post payload exceeds 1 MB limit')
        return v  
    
    
class PostCreate(PostBase):
    """Pydantic model for post creation."""
    pass


class PostResponse(PostBase):
    """
    Pydantic model for post response data.
    
    Attributes:
        id (int): Post ID
        user_id (int): ID of the user who created the post
        created_at (datetime): Timestamp when the post was created
    """
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PostDelete(BaseModel):
    """
    Pydantic model for post deletion request.
    
    Attributes:
        post_id (int): ID of the post to delete
    """
    post_id: int = Field(..., gt=0, description="ID of the post to delete")