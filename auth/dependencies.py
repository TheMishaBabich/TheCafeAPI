from fastapi import Depends, Request, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from db import get_db_session
from .repository import UserRepository
from .services import UserService
from .security import get_existing_user_from_token
from . import User

def get_user_repository(db: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db)

def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)

async def get_current_user(
        request: Request,
        user_service: UserService = Depends(get_user_service)) -> User:
    token = request.cookies.get("TheCafeAPI")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    user_email = await get_existing_user_from_token(token)
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = await user_service.get_user_by_email(user_email)
    return user