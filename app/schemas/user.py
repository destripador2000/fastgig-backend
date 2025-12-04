from pydantic import EmailStr
from sqlmodel import SQLModel
import uuid

class UserBase(SQLModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID