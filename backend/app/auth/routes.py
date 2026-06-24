from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

from app.schemas.user import UserCreate, UserLogin, UserPublic
from app.models.user import User
from app.auth.utils import hash_password, verify_password, create_access_token
from app.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserPublic)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        name=user.name,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserPublic(id=new_user.id, email=new_user.email, name=new_user.name)


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}

