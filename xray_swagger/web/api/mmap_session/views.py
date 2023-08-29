from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from loguru import logger

from xray_swagger.db.dao.mmap_session_dao import MmapSessionDAO

from .schema import MmapSessionCreateDTO, MmapSessionDTO, MmapSessionUpdateDTO

router = APIRouter()


@router.get(path="/sessions", response_model=list[MmapSessionDTO])
async def get_all_mmap_sessions(
    dao: MmapSessionDAO = Depends(),
):
    d = await dao.filter()
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Nothing.")
    logger.debug(d[0].__dict__)
    return d


@router.get(path="/sessions/{uuid}", response_model=MmapSessionDTO)
async def get_mmap_session_by_uuid(
    uuid: UUID,
    dao: MmapSessionDAO = Depends(),
):
    d = await dao.get(uuid)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"MMAP session <uuid: {uuid}> Not Found")
    return d


@router.post(path="/sessions", status_code=status.HTTP_201_CREATED, response_model=MmapSessionDTO)
async def create_mmap_session(
    payload: MmapSessionCreateDTO,
    dao: MmapSessionDAO = Depends(),
):
    logger.debug(payload)
    logger.debug(payload.model_dump(exclude_none=True))
    new = await dao.create(payload)
    return new


@router.patch(path="/sessions/{uuid}", response_model=MmapSessionDTO)
async def update_mmap_session(
    uuid: UUID,
    payload: MmapSessionUpdateDTO,
    dao: MmapSessionDAO = Depends(),
):
    d = await dao.get(uuid)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"MMAP session <uuid: {uuid}> Not Found")

    await dao.update(d, payload)
    return d


@router.delete(path="/sessions/{uuid}", response_description="The mmap session has been removed")
async def delete_mmap_session(
    uuid: UUID,
    dao: MmapSessionDAO = Depends(),
):
    d = await dao.get(uuid)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"MMAP session <uuid: {uuid}> Not Found")

    logger.info(f"Delete mmap session[{d.image_s3_key}]")
    await dao.delete(d)
