from sqlalchemy.orm import Session
from app.exceptions import PostNotFound
from app.schemas.user import UserResponse
from .. import models
from ..schemas import post

def get_all(db: Session):
    return db.query(models.Post).all()

def create(data: post.PostCreate, db: Session, current_user: UserResponse):
    # new_post = models.Post(title = post.title, content=post.content, published=post.published)
    post = models.Post(**data.model_dump(), owner_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_by_id(post_id: int, db: Session):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise PostNotFound
    return post

def delete(post_id: int, db: Session):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    if not post_query.first():
        raise PostNotFound
    post_query.delete(synchronize_session=False)
    db.commit()

def update(post_id: int, data: post.PostUpdate, db: Session):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    if not post_query.first():
        raise PostNotFound
    post_query.update(data.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

def toggle_published(post_id: int, db: Session):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise PostNotFound
    post_query.update({"published": not post.published}, synchronize_session=False)
    db.commit()
    return post_query.first()
