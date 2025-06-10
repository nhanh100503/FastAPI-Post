from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session

from app.models import UserRole
from app.utils import get_current_user, require_role
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from ..database import get_db
from ..services import user_service

router = APIRouter(
    prefix="/users",
    tags=['Users'],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return user_service.get_all(db)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate,
                      db: Session = Depends(get_db),
                      current_user: UserResponse = require_role(UserRole.ADMIN.value)):
    return user_service.create(user, db)

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    return user_service.get_by_id(id, db)

@router.put("/{id}", response_model=UserResponse)
async def update_user(id: int, user_data: UserUpdate,
                      db: Session = Depends(get_db),
                      current_user: UserResponse = require_role(UserRole.ADMIN.value, allow_self_update=True)):
    return user_service.update(id, user_data, db)