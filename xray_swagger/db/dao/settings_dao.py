from __future__ import annotations

import typing

import fastjsonschema
from loguru import logger
from sqlalchemy import and_, select

from xray_swagger.db.dao._base import DAOBase
from xray_swagger.db.models.settings import (
    SettingsGlobal,
    SettingsProduct,
    SettingsProductParameter,
)

if typing.TYPE_CHECKING:
    from xray_swagger.web.api.settings.schema import (
        FullSettingsProductDTO,
        SettingsProductUpdateDTO,
    )


__all__ = (
    "SettingsProductParameterDAO",
    "SettingsProductDAO",
    "SettingsGlobalDAO",
)


class SettingsProductParameterDAO(DAOBase):
    async def get(self, setting_param_name: str) -> SettingsProductParameter:
        raw = await self.session.execute(
            select(SettingsProductParameter).where(
                SettingsProductParameter.setting_param_name == setting_param_name,
            ),
        )
        return raw.scalar()

    async def get_all(self) -> list[SettingsProductParameter]:
        raw = await self.session.execute(select(SettingsProductParameter))
        return list(raw.scalars().fetchall())

    async def filter(self, name_query: str) -> list[SettingsProductParameter]:
        raw = await self.session.execute(
            select(SettingsProductParameter).where(
                SettingsProductParameter.setting_param_name.like(name_query),
            ),
        )
        return list(raw.scalars().fetchall())


class SettingsProductDAO(DAOBase):
    async def create(self, payload: "FullSettingsProductDTO"):
        async with self.session.begin_nested():
            new_settings_product = SettingsProduct(**payload.model_dump(exclude_unset=True))
            print(new_settings_product)
            self.session.add(new_settings_product)

    async def filter_by_product(self, product_id: int) -> list[SettingsProduct]:
        raw = await self.session.execute(
            select(SettingsProduct).where(SettingsProduct.product_id == product_id),
        )
        return list(raw.scalars().fetchall())

    async def get(
        self,
        product_id: int,
        setting_param_name: FullSettingsProductDTO,
    ) -> SettingsProduct:
        raw = await self.session.execute(
            select(SettingsProduct).where(
                and_(
                    SettingsProduct.product_id == product_id,
                    SettingsProduct.setting_param_name == setting_param_name,
                ),
            ),
        )
        return raw.scalar()

    async def update(self, db_obj: SettingsProduct, payload: SettingsProductUpdateDTO) -> None:
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


class SettingsGlobalDAO(DAOBase):
    async def get(self, setting_param_name: str) -> SettingsGlobal:
        raw = await self.session.execute(
            select(SettingsGlobal).where(
                SettingsGlobal.setting_param_name == setting_param_name,
            ),
        )
        return raw.scalar()

    async def get_all(self) -> list[SettingsGlobal]:
        raw = await self.session.execute(select(SettingsGlobal))
        return list(raw.scalars().fetchall())

    async def update(self, db_obj: SettingsGlobal, update_value) -> None:
        json_validator = fastjsonschema.compile(db_obj.json_schema)
        new_value = json_validator(update_value)
        async with self.session.begin_nested():
            db_obj.value = new_value


# class SettingsProductChangelogDAO(IDAO): ...
