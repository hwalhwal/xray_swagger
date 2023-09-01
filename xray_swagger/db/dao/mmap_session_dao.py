from __future__ import annotations

import typing

from loguru import logger
from sqlalchemy import select

from xray_swagger.db.dao._base import DAOBase
from xray_swagger.db.models.mmap_session import MmapSession

if typing.TYPE_CHECKING:
    from xray_swagger.web.api.mmap_session.schema import (
        MmapSessionCreateDTO,
        MmapSessionUpdateDTO,
    )


__all__ = ("MmapSessionDAO",)


class MmapSessionDAO(DAOBase):
    async def create(self, payload: "MmapSessionCreateDTO") -> MmapSession:
        async with self.session.begin_nested():
            new_row = MmapSession(**payload.model_dump(exclude_none=True))
            self.session.add(new_row)

        return new_row

    async def get(self, uuid: str) -> MmapSession:
        raw = await self.session.execute(
            select(MmapSession).where(
                MmapSession.uuid == uuid,
            ),
        )
        return raw.scalar()

    async def get_all(self) -> list[MmapSession]:
        raw = await self.session.execute(select(MmapSession))
        return list(raw.scalars().fetchall())

    async def filter(self) -> list[MmapSession]:
        # TODO: filter query
        q = [MmapSession.is_preserved == True]
        raw = await self.session.execute(
            select(MmapSession).filter(*q),
        )
        return list(raw.scalars().fetchall())

    async def update(self, db_obj: MmapSession, payload: MmapSessionUpdateDTO) -> None:
        refined_update_fields = payload.model_dump(exclude_unset=True)
        logger.debug(f"{refined_update_fields=}")
        for k in refined_update_fields.keys():
            logger.debug(f"{type(db_obj).__name__}.{k} = {db_obj.__getattribute__(k)}")
        # UPDATE FIELDS
        async with self.session.begin_nested():
            logger.debug(f"=== UPDATE {type(db_obj).__name__} ===")
            for k, v in refined_update_fields.items():
                db_obj.__setattr__(k, v)

        for k in refined_update_fields.keys():
            logger.debug(f"{type(db_obj).__name__}.{k} = {db_obj.__getattribute__(k)}")

    async def delete(self, db_obj: MmapSession) -> None:
        async with self.session.begin_nested():
            await self.session.delete(db_obj)
