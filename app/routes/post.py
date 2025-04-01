from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.models import User
from app.schemas.schemas import PostCreate, PostResponse, PostDelete
from app.services.post_service import PostService
from app.repositories.post_repository import PostRepository
from app.core.auth import get_current_user
from app.core.cache import timed_cache

router = APIRouter(tags=["Posts"])

@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def add_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new post.
    
    Args:
        post_data (PostCreate): Post data with text content
        current_user (User): Authenticated user creating the post
        db (Session): Database session
        
    Returns:
        PostResponse: The created post
    """
    post_repository = PostRepository(db)
    post_service = PostService(post_repository)
    
    post = post_service.create_post(post_data.text, current_user)
    
    return PostResponse.from_orm(post)

@router.get("/posts", response_model=List[PostResponse])
@timed_cache(seconds=300)  # Cache for 5 minutes
async def get_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all posts for the authenticated user.
    
    Args:
        current_user (User): Authenticated user
        db (Session): Database session
        
    Returns:
        List[PostResponse]: List of the user's posts
    """
    post_repository = PostRepository(db)
    post_service = PostService(post_repository)
    
    posts = await post_service.get_user_posts(current_user)
    
    return posts

@router.delete("/posts", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_data: PostDelete,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a post.
    
    Args:
        post_data (PostDelete): Post deletion data with post_id
        current_user (User): Authenticated user who owns the post
        db (Session): Database session
        
    Returns:
        None
        
    Raises:
        HTTPException: If the post doesn't exist or doesn't belong to the user
    """
    post_repository = PostRepository(db)
    post_service = PostService(post_repository)
    
    deleted = post_service.delete_post(post_data.post_id, current_user)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or doesn't belong to the authenticated user"
        )