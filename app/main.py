from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.models import Base
from app.db.database import engine
from app.routes import user, post
from app.core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A social media API with user authentication and post management",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(post.router)

@app.get("/")
def read_root():
    """Root endpoint that returns a welcome message."""
    return {"message": f"Welcome to {settings.APP_NAME}!"}