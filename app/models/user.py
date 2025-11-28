from sqlmodel import Field,SQLModel
import uuid
from datetime import datetime
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    full_name: str | None =Field(default=None)
    is_active: bool = Field(default=True)
    role: str =Field(default="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)