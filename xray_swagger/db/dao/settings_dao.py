import fastjsonschema
from sqlalchemy import select

from xray_swagger.db.dao._base import DAOBase
from xray_swagger.db.models.settings import (
    SettingsGlobal,
    SettingsProduct,
    SettingsProductParameter,
)

__all__ = [
    "SettingsProductParameterDAO",
    "SettingsProductDAO",
    "SettingsGlobalDAO",
]


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
    async def filter_by_product(self, product_id: int) -> list[SettingsProduct]:
        raw = await self.session.execute(
            select(SettingsProduct).where(SettingsProduct.product_id == product_id),
        )
        return list(raw.scalars().fetchall())


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
        db_obj.value = new_value
        await self.session.commit()
        await self.session.refresh(db_obj)


# class SettingsProductChangelogDAO(IDAO): ...
