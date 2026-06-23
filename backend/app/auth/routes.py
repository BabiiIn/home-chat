from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.schemas.user import UserCreate, UserLogin, UserPublic
from app.models.user import User
from app.auth.utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# Временное хранилище пользователей (пока нет базы)
fake_users_db = {}
user_id_counter = 1

@router.post("/register", response_model=UserPublic)
def register(user: UserCreate):
    global user_id_counter

    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        id=user_id_counter,
        email=user.email,
        name=user.name,
        password_hash=hash_password(user.password),
        created_at=datetime.utcnow()
    )

    fake_users_db[user.email] = new_user
    user_id_counter += 1

    return UserPublic(id=new_user.id, email=new_user.email, name=new_user.name)

@router.post("/login")
def login(data: UserLogin):
    if data.email not in fake_users_db:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    user = fake_users_db[data.email]

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}
