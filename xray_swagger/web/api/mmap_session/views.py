from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from loguru import logger

from xray_swagger.db.dao.mmap_session_dao import MmapSessionDAO

from .schema import MmapSessionCreateDTO, MmapSessionDTO, MmapSessionUpdateDTO

router = APIRouter()


@router.get(path="/sessions")
async def get_all_mmap_sessions(
    dao: MmapSessionDAO = Depends(),
) -> Sequence[MmapSessionDTO]:
    d = await dao.filter()
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Nothing.")
    logger.debug(d[0].__dict__)
    return d


@router.get(path="/sessions/{uuid}")
async def get_mmap_session_by_uuid(
    uuid: UUID,
    dao: MmapSessionDAO = Depends(),
) -> MmapSessionDTO:
    d = await dao.get(uuid)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"MMAP session <uuid: {uuid}> Not Found")
    return d


@router.post(path="/sessions", status_code=status.HTTP_201_CREATED)
async def create_mmap_session(
    payload: MmapSessionCreateDTO,
    dao: MmapSessionDAO = Depends(),
) -> MmapSessionDTO:
    logger.debug(payload)
    logger.debug(payload.model_dump(exclude_none=True))
    new = await dao.create(payload)
    return new


@router.patch(path="/sessions/{uuid}")
async def update_mmap_session(
    uuid: UUID,
    payload: MmapSessionUpdateDTO,
    dao: MmapSessionDAO = Depends(),
) -> MmapSessionDTO:
    d = await dao.get(uuid)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"MMAP session <uuid: {uuid}> Not Found")

    await dao.update(d, payload, exclude_none=True)
    return d


@router.delete(
    path="/sessions/{uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="The mmap session has been removed",
)
async def delete_mmap_session(
    uuid: UUID,
    dao: MmapSessionDAO = Depends(),
) -> None:
    # noqa: E501
    # TODO: sqlalchemy.exc.IntegrityError: (sqlalchemy.dialects.postgresql.asyncpg.IntegrityError)
    # <class 'asyncpg.exceptions.ForeignKeyViolationError'>: update or delete
    # on table "mmap_session" violates foreign key constraint
    # "inspection_session_end_mmap_session_uuid_fkey"
    # on table "inspection_session"
    #  DETAIL:  Key (uuid)=(76f85d2a-ccf4-4a9e-bd92-f98135d9e164) is still referenced from table
    # "inspection_session".
    d = await dao.get(uuid)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"MMAP session <uuid: {uuid}> Not Found")

    logger.info(f"Delete mmap session[{d.image_s3_key}]")
    await dao.delete(d)
