from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import ConnectionPool, Redis

from xray_swagger.db.dao.user_dao import UserDAO
from xray_swagger.services.redis.dependency import get_redis_pool
from xray_swagger.web.api.deps import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
)

router = APIRouter()


# @router.post("/signup")
# async def singup():
#     return


# @router.post("/signin")
# async def signin():
#     return


# @router.post("/signout")
# async def signout():
#     return


# @router.get("/me")
# async def me():
#     return


# @router.post("/update_profile")
# async def update_profile() -> int:
#     return 0

# @router.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": user.username, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_dao: UserDAO = Depends(),
    redis_pool: ConnectionPool = Depends(get_redis_pool),
):
    user = await authenticate_user(form_data.username, form_data.password, user_dao)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    async with Redis(connection_pool=redis_pool) as redis:
        await redis.set(
            name=f"user_access_token_{user.username}",
            value=access_token,
            keepttl=ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    return {"access_token": access_token, "token_type": "bearer"}
