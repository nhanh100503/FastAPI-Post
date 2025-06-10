from datetime import datetime
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str
    published: bool
    
    class Config:
        from_attributes = True  # Quan trọng để FastAPI có thể sử dụng ORM object (SQLAlchemy)
        
class PostUpdate(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True  # Quan trọng để FastAPI có thể sử dụng ORM object (SQLAlchemy)
        
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Quan trọng để FastAPI có thể sử dụng ORM object (SQLAlchemy)