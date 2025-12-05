from fastapi import APIRouter
from fastapi.params import Depends
from app.db.session import get_session
from app.models import User
from app.schemas.user import UserCreate
from app.schemas.user import UserRead
from app.core.security import hash_password
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):

    pass_hash = hash_password(user.password)

    new_user = User(
        email=user.email,
        hashed_password= pass_hash,
        full_name=user.full_name,
        is_active=user.is_active
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user