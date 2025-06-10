from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole
    
    class config:
        from_attributes: True
        
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    
    class config:
        from_attributes: True
        
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    role: UserRole
    
    class config:
        from_attributes: True
        
