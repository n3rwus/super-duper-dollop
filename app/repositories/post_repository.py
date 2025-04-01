from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import Post, User

class PostRepository:
    """
    Repository class for Post-related database operations.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.
        
        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db
    
    def create_post(self, text: str, user_id: int) -> Post:
        """
        Create a new post.
        
        Args:
            text (str): Content of the post
            user_id (int): ID of the post's author
            
        Returns:
            Post: The created post object
        """
        post = Post(text=text, user_id=user_id)
        
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        
        return post
    
    def get_user_posts(self, user_id: int) -> List[Post]:
        """
        Retrieve all posts for a specific user.
        
        Args:
            user_id (int): User ID to get posts for
            
        Returns:
            List[Post]: List of Post objects
        """
        return self.db.query(Post).filter(Post.user_id == user_id).all()
    
    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        """
        Retrieve a post by ID.
        
        Args:
            post_id (int): Post ID to search for
            
        Returns:
            Optional[Post]: Post object if found, None otherwise
        """
        return self.db.query(Post).filter(Post.id == post_id).first()
    
    def delete_post(self, post_id: int, user_id: int) -> bool:
        """
        Delete a post if it belongs to the specified user.
        
        Args:
            post_id (int): ID of the post to delete
            user_id (int): ID of the user who owns the post
            
        Returns:
            bool: True if the post was deleted, False otherwise
        """
        post = self.db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
        
        if not post:
            return False
            
        self.db.delete(post)
        self.db.commit()
        
        return True