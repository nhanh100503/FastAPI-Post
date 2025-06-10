from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey, Enum
from .database import Base
from sqlalchemy.orm import relationship
import enum

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class BaseModel:
    id = Column(Integer, primary_key=True, index=True, nullable=False)

class Post(Base, BaseModel):
    __tablename__ = "posts"
    
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="true")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base, BaseModel):
    __tablename__ = "users"
    
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    role = Column(Enum(UserRole), nullable=False, server_default="USER")  
    
class RefreshToken(Base, BaseModel):
    __tablename__ = "refresh_token"
    
    token = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User")