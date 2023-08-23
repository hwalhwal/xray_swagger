import starlette.status as stc
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from loguru import logger

from xray_swagger.db.dao.user_dao import UserDAO

from .schema import UserCreateDTO, UserModelDTO, UserUpdateDTO

router = APIRouter()


@router.post(path="/", response_model=UserModelDTO)
async def create_user(
    *,
    new_user_obj: UserCreateDTO,
    user_dao: UserDAO = Depends(),
):
    if user_dupl := await user_dao.get_by_username(new_user_obj.username):
        logger.warning(f"User name: {user_dupl.username} Fullname: {user_dupl.fullname}")
        raise HTTPException(
            status_code=stc.HTTP_409_CONFLICT,
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


@router.get(path="/", response_model=list[UserModelDTO])
async def read_all_user(
    *,
    user_dao: UserDAO = Depends(),
):
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
            status_code=stc.HTTP_404_NOT_FOUND,
            detail="Specified user not found",
        )
    print(user)
    print(user.__dict__)
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
            status_code=stc.HTTP_404_NOT_FOUND,
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
            status_code=stc.HTTP_404_NOT_FOUND,
            detail="Specified user not found",
        )
    logger.info(f"Delete user[{user.username}]")

    await user_dao.delete(user)
