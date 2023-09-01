from datetime import datetime
from typing import Generic, Sequence, TypeVar, get_args

from fastapi import Depends
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from xray_swagger.db.base import Base
from xray_swagger.db.dependencies import get_db_session

ModelType = TypeVar("ModelType", bound=Base)
CreateDTOType = TypeVar("CreateDTOType", bound=BaseModel)
UpdateDTOType = TypeVar("UpdateDTOType", bound=BaseModel)


class DAOBase(Generic[ModelType, CreateDTOType, UpdateDTOType]):
    """Base Class for DAO."""

    MODEL: ModelType

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        logger.debug(f"CLASS <{cls.__name__}>")
        logger.debug(f"{cls.__orig_bases__=}")
        # subclass에서 Generic 0의 orm Model class를 획득할 수 있다.
        cls.MODEL = get_args(cls.__orig_bases__[0])[0]

    async def create(self, payload: CreateDTOType) -> ModelType:
        logger.debug(f"=== CREATE {self.MODEL.__name__}")
        async with self.session.begin_nested():
            new_row = self.MODEL(**payload.model_dump(exclude_none=True))
            self.session.add(new_row)
        return new_row

    async def get(self, id: int) -> ModelType | None:
        logger.debug(f"=== GET 1 {self.MODEL.__name__}")
        row = await self.session.execute(
            select(self.MODEL).where(self.MODEL.id == id),
        )
        return row.scalar()

    async def get_all(self) -> Sequence[ModelType]:
        logger.debug(f"=== GET ALL {self.MODEL.__name__}")
        rows = await self.session.execute(select(self.MODEL))
        return rows.scalars().fetchall()

    async def update(
        self,
        db_obj: ModelType,
        payload: UpdateDTOType,
        *,
        exclude_none: bool = False,
        exclude_unset: bool = False,
    ) -> None:
        refined_update_fields = payload.model_dump(
            exclude_none=exclude_none,
            exclude_unset=exclude_unset,
        )
        logger.debug(f"{refined_update_fields=}")
        for k in refined_update_fields.keys():
            logger.debug(f"{type(db_obj).__name__}.{k} = {db_obj.__getattribute__(k)}")
        # UPDATE FIELDS
        async with self.session.begin_nested():
            logger.debug(f"=== UPDATE {type(db_obj).__name__}")
            for k, v in refined_update_fields.items():
                db_obj.__setattr__(k, v)

        for k in refined_update_fields.keys():
            logger.debug(f"{type(db_obj).__name__}.{k} = {db_obj.__getattribute__(k)}")

    async def delete(self, db_obj: ModelType) -> None:
        logger.debug(f"=== DELETE {type(db_obj).__name__}")
        async with self.session.begin_nested():
            await self.session.delete(db_obj)

    async def quasi_delete(self, db_obj: ModelType) -> None:
        logger.debug(f"=== quasi-DELETE {type(db_obj).__name__} by setting column `deleted_at`")
        async with self.session.begin_nested():
            db_obj.deleted_at = datetime.utcnow()
