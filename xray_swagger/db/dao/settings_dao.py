from __future__ import annotations

from typing import Sequence

from sqlalchemy import and_, select

from xray_swagger.db.dao._base import IDAO, DAOBase
from xray_swagger.db.models.settings import (
    SettingsGlobal,
    SettingsProduct,
    SettingsProductChangelog,
    SettingsProductParameter,
)
from xray_swagger.web.api.settings.schema import (
    SettingsGlobalUpdateDTO,
    SettingsProductChangelogCreateDTO,
    SettingsProductCreateDTO,
    SettingsProductUpdateDTO,
)

__all__ = (
    "SettingsProductParameterDAO",
    "SettingsProductDAO",
    "SettingsGlobalDAO",
    "SettingsProductChangelogDAO",
)


class SettingsProductParameterDAO(IDAO):
    async def get(self, setting_param_name: str) -> SettingsProductParameter:
        raw = await self.session.execute(
            select(SettingsProductParameter).where(
                SettingsProductParameter.setting_param_name == setting_param_name,
            ),
        )
        return raw.scalar()

    async def get_all(self) -> Sequence[SettingsProductParameter]:
        raw = await self.session.execute(select(SettingsProductParameter))
        return raw.scalars().fetchall()

    async def filter(self, name_query: str) -> Sequence[SettingsProductParameter]:
        raw = await self.session.execute(
            select(SettingsProductParameter).where(
                SettingsProductParameter.setting_param_name.like(name_query),
            ),
        )
        return raw.scalars().fetchall()


class SettingsProductDAO(
    DAOBase[SettingsProduct, SettingsProductCreateDTO, SettingsProductUpdateDTO],
):
    async def filter_by_product(self, product_id: int) -> Sequence[SettingsProduct]:
        raw = await self.session.execute(
            select(SettingsProduct).where(SettingsProduct.product_id == product_id),
        )
        return raw.scalars().fetchall()

    async def get(
        self,
        product_id: int,
        setting_param_name: str,
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


class SettingsGlobalDAO(
    DAOBase[SettingsGlobal, None, SettingsGlobalUpdateDTO],
):
    async def get(self, setting_param_name: str) -> SettingsGlobal:
        raw = await self.session.execute(
            select(SettingsGlobal).where(
                SettingsGlobal.setting_param_name == setting_param_name,
            ),
        )
        return raw.scalar()

    async def get_all(self) -> Sequence[SettingsGlobal]:
        raw = await self.session.execute(select(SettingsGlobal))
        return raw.scalars().fetchall()


class SettingsProductChangelogDAO(
    DAOBase[SettingsProductChangelog, SettingsProductChangelogCreateDTO, None],
):
    async def filter(
        self,
        product_id: int,
        name_query: str,
    ) -> Sequence[SettingsProductChangelog]:
        q = [SettingsProductChangelog.product_id == product_id]
        if name_query:
            q.append(SettingsProductChangelog.setting_param_name.like(name_query))
        raw = await self.session.execute(
            select(SettingsProductChangelog).filter(*q),
        )
        return raw.scalars().fetchall()
