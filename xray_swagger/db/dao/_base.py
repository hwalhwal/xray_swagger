from typing import Generic, Sequence, TypeVar

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

    model = ModelType

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create(self, payload: CreateDTOType) -> ModelType:
        logger.debug(f"=== CREATE {ModelType.__name__}")
        async with self.session.begin_nested():
            new_product = ModelType(**payload.model_dump(exclude_none=True))
            self.session.add(new_product)
        return new_product

    async def get(self, id: int) -> ModelType | None:
        logger.debug(f"=== GET 1 {ModelType.__name__}")
        raw = await self.session.execute(
            select(self.model).where(self.model.id == id),
        )
        return raw.scalar()

    async def get_all(self) -> Sequence[ModelType]:
        logger.debug(f"=== GET ALL {ModelType.__name__}")
        raw = await self.session.execute(select(ModelType))
        return raw.scalars().fetchall()

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
