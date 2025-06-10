from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.schemas import post, user
from . import models
from app.database import Base, SessionLocal, engine
from app.routers import user, post, auth
from app.exceptions import register_all_errors
from sqlalchemy.orm import Session
from app.utils import hash

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

register_all_errors(app)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        create_default_user(db)
    finally:
        db.close()
    yield  
    
app.router.lifespan_context = lifespan

def create_default_user(db: Session):
    default_user = db.query(models.User).filter_by(email="admin@example.com").first()
    if not default_user:
        new_user = models.User(
            name="Admin User",
            email="admin@example.com",
            password=hash("defaultpassword123"),
            role=models.UserRole.ADMIN
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print("Default admin user created!")
    else:
        print("Default admin user already exists!")