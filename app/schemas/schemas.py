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