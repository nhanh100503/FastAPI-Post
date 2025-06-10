from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from app.schemas.auth import RefreshTokenRequest, Login
from app.database import get_db
from app.services import auth_service
from app.utils import refresh_access_token

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post("/login")
async def login(user_credentials: Login, db: Session = Depends(get_db)):
    return auth_service.login(user_credentials, db)

@router.post("/token/refresh")
def refresh_token(refresh_token: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_access_token(refresh_token, db)