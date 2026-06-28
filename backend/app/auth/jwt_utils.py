from jose import jwt, JWTError
from fastapi import HTTPException, status

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # здесь будет user_id, email и т.д.
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
