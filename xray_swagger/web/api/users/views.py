from typing import Annotated

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.param_functions import Depends
from loguru import logger

from xray_swagger.db.dao.user_dao import UserDAO
from xray_swagger.web.api.deps import get_current_active_user
from xray_swagger.web.middlewares.permissions import (
    IsAuthenticated,
    IsSupervisor,
    PermissionsDependency,
)

from .schema import UserCreateDTO, UserModelDTO, UserUpdateDTO

router = APIRouter()


@router.get("/me")
def read_current_user(
    user: Annotated[UserModelDTO, Depends(get_current_active_user)],
) -> UserModelDTO:
    logger.debug(type(user))
    logger.debug(user)
    return user


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated, IsSupervisor]))],
    response_model=UserModelDTO,
)
async def create_user(
    *,
    new_user_obj: UserCreateDTO,
    user_dao: UserDAO = Depends(),
):
    if user_dupl := await user_dao.get_by_username(new_user_obj.username):
        logger.warning(f"User name: {user_dupl.username} Fullname: {user_dupl.fullname}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that username already exists.",
        )

    new_user = await user_dao.create(
        **new_user_obj.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )
    )
    logger.info(new_user.__dict__)
    # return UserModelDTO.model_validate(new_user)
    return new_user


@router.get(path="/schema")
async def get_user_schema_json():
    """유저 생성에 필요한 JSON schema를 반환합니다."""
    return UserCreateDTO.model_json_schema()


@router.get(
    path="/",
    response_model=list[UserModelDTO],
)
async def read_all_user(
    *,
    request: Request,
    authorize: bool = Depends(PermissionsDependency([IsAuthenticated, IsSupervisor])),
    user_dao: UserDAO = Depends(),
):
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


@router.get(path="/{user_id}", response_model=UserModelDTO)
async def read_user_by_id(
    *,
    user_id: int,
    user_dao: UserDAO = Depends(),
) -> UserModelDTO:
    user = await user_dao.get_by_id(user_id)

    if not user:
        # TODO: HTTP Exceptions -> NotFoundUserException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified user not found",
        )
    print(user.__dict__)
    # return UserModelDTO.model_validate(user)
    return user


@router.put(path="/{user_id}", response_model=UserModelDTO)
async def update_user(
    *,
    user_id: int,
    update_payload: UserUpdateDTO,
    user_dao: UserDAO = Depends(),
):
    user = await user_dao.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified user not found",
        )
    logger.info(
        f"Update user[{user.username}] with: {update_payload.model_dump(exclude_none=True)}",
    )
    user = await user_dao.update(user, update_payload)

    return user


@router.delete(
    path="/{user_id}",
    response_description="The user has been removed",
)
async def delete_user(
    *,
    user_id: int,
    user_dao: UserDAO = Depends(),
):
    user = await user_dao.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified user not found",
        )
    logger.info(f"Delete user[{user.username}]")

    await user_dao.delete(user)
