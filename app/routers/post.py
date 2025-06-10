from fastapi import Depends, status, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session

from app.schemas.user import UserResponse
from app.utils import get_current_user
from ..schemas import post
from .. import models
from ..database import get_db
from ..services import post_service

router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=list[post.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    return post_service.get_all(db)

@router.post("/", response_model=post.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: post.PostCreate,
                      db: Session = Depends(get_db),
                      current_user: UserResponse = Depends(get_current_user)):
    return post_service.create(post, db, current_user)

@router.get("/{id}", response_model=post.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    return post_service.get_by_id(id, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post_service.delete(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=post.PostResponse)
async def update_post(id: int, post_data: post.PostUpdate, db: Session = Depends(get_db)):
    return post_service.update(id, post_data, db)

@router.put("/update-published/{id}", response_model=post.PostResponse)
async def update_published_post(id: int, db: Session = Depends(get_db)):
    return post_service.toggle_published(id, db)
