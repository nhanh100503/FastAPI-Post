from app.exceptions import EmailNotFound, InvalidPassword
from app.schemas.user import UserResponse
from app.models import RefreshToken, User
from app.utils import create_access_token, create_refresh_token, verify_password
from ..schemas import auth
from sqlalchemy.orm import Session

def login(data: auth.Login, db: Session):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise EmailNotFound
    if not verify_password(data.password, user.password):
        raise InvalidPassword
    user_payload = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value
    }
    access_token = create_access_token(user_data=user_payload)
    refresh_token = create_refresh_token(user_data=user_payload)
    
    existing_token = db.query(RefreshToken).filter(RefreshToken.user_id == user.id).first()
    if existing_token:
        existing_token.token = refresh_token 
    else:
        db.add(RefreshToken(token=refresh_token, user_id=user.id))
    db.commit()
    
    return auth.AuthLoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(id=user.id, name=user.name, email=user.email, created_at=user.created_at, role=user.role.value)
    )