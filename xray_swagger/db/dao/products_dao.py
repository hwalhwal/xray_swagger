from __future__ import annotations

from typing import Sequence

from sqlalchemy import and_, select

from xray_swagger.db.dao._base import DAOBase
from xray_swagger.db.models.defect import Defect, DefectCategory
from xray_swagger.db.models.product import InspectionSession, Product
from xray_swagger.web.api.products.schema import (
    DefectCreateDTO,
    DefectUpdateDTO,
    InspectionSessionCreateDTO,
    InspectionSessionUpdateDTO,
    ProductCreateDTO,
)

# import sqlalchemy.orm as orm


__all__ = ("ProductDAO", "InspectionSessionDAO", "DefectDAO")


class ProductDAO(DAOBase[Product, ProductCreateDTO, ProductCreateDTO]):
    async def get_all(self, offset: int = 0, limit: int = 20) -> Sequence[Product]:
        raw = await self.session.execute(
            select(Product).offset(offset).limit(limit),
        )
        return raw.scalars().fetchall()

    async def filter(self, name_query: str) -> Sequence[Product]:
        raw = await self.session.execute(
            select(Product).where(
                Product.name.like(name_query),
            ),
        )
        return raw.scalars().fetchall()


class InspectionSessionDAO(
    DAOBase[InspectionSession, InspectionSessionCreateDTO, InspectionSessionUpdateDTO],
):
    async def get_all(
        self,
        product_id: int,
        offset: int = 0,
        limit: int = 20,
    ) -> Sequence[InspectionSession]:
        raw = await self.session.execute(
            select(InspectionSession)
            .where(InspectionSession.product_id == product_id)
            .offset(offset)
            .limit(limit),
        )
        return raw.scalars().fetchall()

    async def get_by_id(self, product_id: int, id: int) -> InspectionSession:
        raw = await self.session.execute(
            select(InspectionSession).where(
                and_(
                    InspectionSession.product_id == product_id,
                    InspectionSession.id == id,
                ),
            ),  # .options(orm.selectinload(InspectionSession.product)),
        )
        return raw.scalar()

    async def filter(self, product_id: int) -> Sequence[InspectionSession]:
        # TODO: time range query
        raw = await self.session.execute(
            select(InspectionSession).where(
                InspectionSession.product_id == product_id,
            ),
        )
        return raw.scalars().fetchall()


class DefectDAO(DAOBase[Defect, DefectCreateDTO, DefectUpdateDTO]):
    async def filter(
        self,
        product_id: int,
        isp_sess_id: int | None = None,
        defect_category: DefectCategory | None = None,
    ) -> Sequence[Defect]:
        q = [Defect.product_id == product_id]
        if isp_sess_id:
            q.append(Defect.inspection_session_id == isp_sess_id)
        if defect_category:
            q.append(Defect.defect_category == defect_category)

        raw = await self.session.execute(
            select(Defect).filter(*q),
        )
        return raw.scalars().fetchall()
