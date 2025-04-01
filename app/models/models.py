from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    
    """
    SQLAlchemy model for user data.
    
    Attributes:
        id (int): Primary key for the user
        email (str): Unique email address for the user
        password (str): Hashed password for authentication
        created_at (datetime): Timestamp when the user was created
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationship with Post model
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    
class Post(Base):
    """
    SQLAlchemy model for post data.
    
    Attributes:
        id (int): Primary key for the post
        text (str): Content of the post
        user_id (int): Foreign key referencing the post's author
        created_at (datetime): Timestamp when the post was created
    """
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationship with User model
    author = relationship("User", back_populates="posts")