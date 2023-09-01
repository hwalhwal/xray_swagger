import secrets
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger
from pydantic import BaseModel

from xray_swagger.db.dao.user_dao import UserDAO
from xray_swagger.db.models.user import User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


SECRET_KEY = "b047ec65b80608f1c1fcd10d640cc6f88fce63ce18a5cf085c0c5fd18c820c04"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


security = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password, hashed_password) -> bool:
    # return pwd_context.verify(plain_password, hashed_password)
    return secrets.compare_digest(
        plain_password,
        hashed_password,
    )


def get_password_hash(password):
    # return pwd_context.hash(password)
    return password


async def authenticate_user(username: str, password: str, user_dao: UserDAO) -> User | None:
    user = await user_dao.get_by_username(username)
    if not user:
        return
    if not verify_password(password, user.password):
        return
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(security)],
    user_dao: UserDAO = Depends(),
) -> User:
    CredentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.debug(type(token))
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(payload)
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException
    user = await user_dao.get_by_username(token_data.username)
    if user is None:
        raise CredentialsException

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.deleted_at:
        logger.warning(f"User {current_user.username} was deleted at {current_user.deleted_at}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
