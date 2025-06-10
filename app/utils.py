from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from jwt.exceptions import InvalidTokenError
from app import models
from app.exceptions import ExpiredToken, InvalidToken, InvalidUserToken, UserNotFound
from app.schemas.auth import RefreshTokenRequest
from app.schemas.user import UserResponse
from .config import settings
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request, status, Depends, Header
from sqlalchemy.orm import Session
from app.database import get_db


SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)

def create_access_token(user_data: dict, refresh: bool = False) -> str:
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user": user_data,
        "exp": int(expire_time.timestamp()),
        "refresh": refresh
    }
    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_data: dict, refresh: bool = True) -> str:
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user": user_data,
        "exp": int(expire_time.timestamp()),
        "refresh": refresh
    }
    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, expected_refresh: bool) -> dict:
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("refresh") != expected_refresh:
            raise InvalidTokenError("Loại token không hợp lệ")
        return payload["user"]
    except ExpiredSignatureError:
        raise ExpiredToken
    except InvalidTokenError:
        raise InvalidToken
        
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserResponse:
    user_data = verify_token(token, expected_refresh=False)
    user = db.query(models.User).filter(models.User.id == user_data["id"]).first()
    if user is None:
        raise UserNotFound
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
        role=user.role.value
    )

def require_role(required_role: str, allow_self_update: bool = False, user_id_param: str = "id"):
    async def dependency(
        request: Request,
        current_user: UserResponse = Depends(get_current_user),
    ):
        user_id = int(request.path_params.get(user_id_param, 0))
        if current_user.role != required_role:
            if allow_self_update and current_user.id == user_id:
                return current_user
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Require role '{required_role}'"
            )
        return current_user
    return Depends(dependency)


def refresh_access_token(data: RefreshTokenRequest, db: Session):
    token_str = data.refresh_token 
    token_in_db = db.query(models.RefreshToken).filter(models.RefreshToken.token == token_str).first()
    if not token_in_db:
        raise InvalidToken
    user_data = verify_token(token_str, expected_refresh=True)
    new_access_token = create_access_token(user_data=user_data)
    return {"access_token": new_access_token}
