from fastapi import APIRouter
from app.core.config import Settings
from app.models import User
from app.schemas.user import UserCreate
from app.schemas.user import UserRead
from app.core.security import get_password_hash
router = APIRouter()

@router.post("/users")
async def create_user(user: UserCreate, get_session: Settings):

    pass_hash = get_password_hash(user.password)

    new_user = User(
        email=user.email,
        hashed_password= pass_hash,
        full_name=user.full_name,
        is_active=user.is_active,
        role=user.role,
    )

    get_session.add(new_user)
    await get_session.commit()
    await get_session.refresh(new_user)
    return UserRead