from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Это временная модель (in-memory), пока мы не подключили PostgreSQL.
# Позже мы заменим её на настоящую ORM-модель.

class User(BaseModel):
    id: int
    email: str
    name: str
    password_hash: str
    created_at: datetime
