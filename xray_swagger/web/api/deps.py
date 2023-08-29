import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from loguru import logger

from xray_swagger.db.dao.user_dao import UserDAO
from xray_swagger.web.api.users.schema import UserModelDTO

security = HTTPBasic()


async def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    user_dao: UserDAO = Depends(),
):
    logger.debug(type(credentials))
    # logger.debug(credentials.__dict__)
    user = await user_dao.get_by_username(credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with username '{credentials.username}' does not exist",
        )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = user.password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes,
        correct_password_bytes,
    )
    if not is_correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(
    current_user: Annotated[UserModelDTO, Depends(get_current_user)],
):
    if current_user.deleted_at:
        logger.warning(f"User {current_user.username} was deleted at {current_user.deleted_at}")
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
