#auth/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.modules.auth.security import hash_password, verify_password, create_access_token


def register_user(email: str, password: str, db: Session):

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    user = User(
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()

    return {"message": "Usuario creado correctamente"}


def login_user(email: str, password: str, db: Session):

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token}