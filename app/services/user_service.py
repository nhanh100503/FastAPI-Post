from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user import UserUpdate, UserCreate, UserResponse
from app.utils import hash
from ..exceptions import UserAlreadyExists, UserNotFound

def get_all(db: Session):
    users = db.query(User).all()
    return users

def create(data: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise UserAlreadyExists
    
    user_data = data.model_dump()
    user_data["password"] = hash(data.password)  
    user_data["role"] = data.role.value.upper() 
    
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFound
    return user

def update(user_id: int, user_data: UserUpdate, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFound
    update_data = user_data.model_dump(exclude_unset=True)
    if "role" in update_data:
        update_data["role"] = user_data.role.value 
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user