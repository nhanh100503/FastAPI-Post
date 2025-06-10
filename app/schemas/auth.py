from pydantic import BaseModel, EmailStr
from app.schemas import user
class Login(BaseModel):
    email: EmailStr
    password: str
    
class AuthLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: user.UserResponse
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str