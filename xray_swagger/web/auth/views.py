from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
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


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_dao: UserDAO = Depends(),
    redis_pool: ConnectionPool = Depends(get_redis_pool),
):
    logger.debug(form_data)
    logger.debug(form_data.__dict__)
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
    redis_key = f"user_access_token_{user.username}"
    async with Redis(connection_pool=redis_pool) as redis:
        if not await redis.get(redis_key):
            await redis.set(
                name=redis_key,
                value=access_token,
            )
        await redis.expire(name=redis_key, time=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
