#auth/controller
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.schemas import UserCreate, TokenResponse
from app.modules.auth.service import register_user, login_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user.email, user.password, db)


@router.post("/login", response_model=TokenResponse)
def login(user: UserCreate, db: Session = Depends(get_db)):
    return login_user(user.email, user.password, db)