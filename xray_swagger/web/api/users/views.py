from typing import Annotated, Any, Sequence

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.param_functions import Depends
from loguru import logger

from xray_swagger.db.dao.user_dao import UserDAO
from xray_swagger.db.models.user import User
from xray_swagger.web.dependencies.permissions import (
    IsAuthenticated,
    IsSupervisor,
    PermissionsDependency,
)
from xray_swagger.web.dependencies.users import get_current_active_user

from .schema import UserCreateDTO, UserModelDTO, UserUpdateDTO, UserUpdateMeDTO

router = APIRouter()


@router.get("/me")
async def read_current_user(
    user: Annotated[User, Depends(get_current_active_user)],
) -> UserModelDTO:
    logger.debug(type(user))
    logger.debug(user)
    return user


@router.patch("/me")
async def update_current_user(
    payload: UserUpdateMeDTO,
    user: Annotated[User, Depends(get_current_active_user)],
    user_dao: UserDAO = Depends(),
) -> UserModelDTO:
    await user_dao.update(user, payload, exclude_none=True)
    return user


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated, IsSupervisor]))],
)
async def create_user(
    payload: UserCreateDTO,
    user_dao: UserDAO = Depends(),
) -> UserModelDTO:
    # NOTE: User sign up 과는 다르다. 관리자 및 엔지니어 다른 유저를 만들수 있다.
    if user_dupl := await user_dao.get_by_username(payload.username):
        logger.warning(f"User name: {user_dupl.username} Fullname: {user_dupl.fullname}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that username already exists.",
        )
    new_user = await user_dao.create(payload)
    logger.info(new_user.__dict__)
    # return UserModelDTO.model_validate(new_user)
    return new_user


@router.get(path="/schema")
async def get_user_schema_json() -> dict[str, Any]:
    """유저 생성에 필요한 JSON schema를 반환합니다."""
    return UserCreateDTO.model_json_schema()


@router.get(path="/")
async def read_all_user(
    request: Request,
    authorize: bool = Depends(PermissionsDependency([IsAuthenticated, IsSupervisor])),
    user_dao: UserDAO = Depends(),
) -> Sequence[UserModelDTO]:
    from pprint import pformat

    logger.debug(request)
    logger.debug(pformat(request.scope))
    logger.debug(pformat(request.headers.__dict__))
    logger.debug(pformat(request.state.__dict__))
    # logger.debug(request.auth)
    # logger.debug(request.user)
    # logger.debug(request.session)
    # logger.debug(pformat(request.__dict__))
    users = await user_dao.get_all()
    logger.info("Getting users list")
    return users


@router.get(path="/{user_id}")
async def read_user_by_id(
    user_id: int,
    user_dao: UserDAO = Depends(),
) -> UserModelDTO:
    user = await user_dao.get(user_id)

    if not user:
        # TODO: HTTP Exceptions -> NotFoundUserException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified user not found",
        )
    print(user.__dict__)
    # return UserModelDTO.model_validate(user)
    return user


@router.patch(
    path="/{user_id}",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated, IsSupervisor]))],
)
async def update_user(
    user_id: int,
    update_payload: UserUpdateDTO,
    user_dao: UserDAO = Depends(),
) -> UserModelDTO:
    # NOTE: 관리자가 유저를 업데이트하는 것이다.
    # 유저가 자기 자신의 정보를 변경할 경우에는 me를 사용한다.

    user = await user_dao.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified user not found",
        )
    await user_dao.update(user, update_payload, exclude_none=True)
    return user


@router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="The user has been removed",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated, IsSupervisor]))],
)
async def delete_user(
    user_id: int,
    user_dao: UserDAO = Depends(),
) -> None:
    user = await user_dao.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified user not found",
        )
    logger.info(f"Delete user[{user.username}]")

    await user_dao.delete(user)
