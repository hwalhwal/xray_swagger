from typing import Sequence

from loguru import logger
from sqlalchemy import select

from xray_swagger.db.dao._base import DAOBase
from xray_swagger.db.models.mmap_session import MmapSession
from xray_swagger.web.api.mmap_session.schema import (
    MmapSessionCreateDTO,
    MmapSessionUpdateDTO,
)

__all__ = ("MmapSessionDAO",)


class MmapSessionDAO(DAOBase[MmapSession, MmapSessionCreateDTO, MmapSessionUpdateDTO]):
    async def get(self, uuid: str) -> MmapSession:
        raw = await self.session.execute(
            select(MmapSession).where(MmapSession.uuid == uuid),
        )
        return raw.scalar()

    async def filter(self) -> Sequence[MmapSession]:
        # TODO: filter query
        logger.debug(f"{self.MODEL.__name__} filter query")
        q = [MmapSession.is_preserved == True]
        raw = await self.session.execute(
            select(MmapSession).filter(*q),
        )
        return raw.scalars().fetchall()
