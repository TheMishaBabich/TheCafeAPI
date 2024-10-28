from datetime import timedelta


from fastapi import Response, Request, HTTPException
from starlette import status

from .security import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

def create_cookie_for_curr_user(response: Response, email: str):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email},
        expires_delta=access_token_expires
    )

    response.set_cookie(
        key="TheCafeAPI",
        value=access_token,
        httponly=True,
        max_age=3600,
        secure=True,
        samesite="Lax"
    )
    return


async def check_active_user(request: Request):
    active_cookie = request.cookies.get("TheCafeAPI")
    if active_cookie is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already logged in.",
        )

def remove_cookie(response: Response):
    response.delete_cookie("TheCafeAPI")
