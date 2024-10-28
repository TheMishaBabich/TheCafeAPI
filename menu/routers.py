from fastapi import APIRouter

from auth import schemas

auth_router = APIRouter()


@auth_router.post("/register", response_model=schemas.User)
async def auth_register():
    return

@auth_router.post("/login", response_model=schemas.User)
async def auth_login():
    return

@auth_router.post("/logout", response_model=schemas.User)
async def auth_logout():
    return

