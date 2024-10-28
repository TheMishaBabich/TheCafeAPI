
from fastapi import HTTPException, status, Request, Response
from sqlalchemy.exc import IntegrityError
from urllib3 import request

from . import User
from .repository import UserRepository
from .schemas import UserLoginRequest, UserRegisterRequest
from .security import hash_password, verify_password
from .utils import check_active_user, remove_cookie


async def logout_user() -> dict:
    return {"message": "Successfully logged out"}


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: UserRegisterRequest, request: Request) -> User:
        user = User(
            email=user_data.email,
            password=hash_password(user_data.password),
            name=user_data.name
        )
        await check_active_user(request)

        try:
            return self.repository.add_user(user)
        except IntegrityError:
            raise HTTPException(
                detail="Email already registered",
                status_code=status.HTTP_400_BAD_REQUEST
            )

    async def get_user_by_email(self, email: str) -> User:
        user = self.repository.get_user_by_email(email)
        if user is None:
            raise HTTPException(
                detail="Email not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        return user

    async def login_user(self, user_data: UserLoginRequest, request: Request) -> User:
        user = self.repository.get_user_by_email(user_data.email)

        await check_active_user(request)

        if user is None:
            raise HTTPException(
                detail="Email not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if not verify_password(user_data.password, user.password):
            raise HTTPException(
                detail="Password mismatch",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return user
    async def logout_user(self, response: Response):
        remove_cookie(response)
        return