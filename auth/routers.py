from fastapi import APIRouter, Depends,  Response
from starlette.requests import Request

from .dependencies import get_user_service, get_current_user
from . import User
from .schemas import UserLoginRespons, UserLoginRequest, UserRegisterResponse, UserRegisterRequest
from .services import UserService
from .utils import create_cookie_for_curr_user

auth_router = APIRouter()


@auth_router.post("/register", response_model=UserRegisterResponse)
async def auth_register(
        user_data: UserRegisterRequest,
        response: Response,
        request: Request,
        user_service: UserService = Depends(get_user_service)
):
    user = await user_service.create_user(user_data, request)
    create_cookie_for_curr_user(response=response, email=user.email)

    return UserRegisterResponse(name=user_data.name, message="You are registered")

@auth_router.post("/login", response_model=UserLoginRespons)
async def auth_login(
    form: UserLoginRequest,
    response: Response,
    request: Request,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.login_user(form, request)
    create_cookie_for_curr_user(response=response, email=user.email)
    return UserLoginRespons(name=user.name, message="You are logged in")

@auth_router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return {"email": current_user.email, "name": current_user.name}

@auth_router.post("/logout")
async def auth_logout(response: Response,
                      user_service: UserService = Depends(get_user_service),
):
    await user_service.logout_user(response)
    return {"message": "You have been logged out"}
