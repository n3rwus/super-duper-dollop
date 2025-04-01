from typing import List
from app.repositories.post_repository import PostRepository
from app.models.models import Post, User
from app.schemas.schemas import PostResponse

class PostService:
    """
    Service class for post-related business logic.
    """
    
    def __init__(self, post_repository: PostRepository):
        """
        Initialize the service with a post repository.
        
        Args:
            post_repository (PostRepository): Repository for post database operations
        """
        self.post_repository = post_repository
    
    def create_post(self, text: str, user: User) -> Post:
        """
        Create a new post for a user.
        
        Args:
            text (str): Content of the post
            user (User): User creating the post
            
        Returns:
            Post: The created post object
        """
        return self.post_repository.create_post(text, user.id)
    
    async def get_user_posts(self, user: User) -> List[PostResponse]:
        """
        Get all posts for a user.
        
        Args:
            user (User): User to get posts for
            
        Returns:
            List[PostResponse]: List of post response objects
        """
        posts = self.post_repository.get_user_posts(user.id)
        return [PostResponse.from_orm(post) for post in posts]
    
    def delete_post(self, post_id: int, user: User) -> bool:
        """
        Delete a post if it belongs to the user.
        
        Args:
            post_id (int): ID of the post to delete
            user (User): User who owns the post
            
        Returns:
            bool: True if the post was deleted, False otherwise
        """
        return self.post_repository.delete_post(post_id, user.id)