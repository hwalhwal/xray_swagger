from __future__ import annotations

import typing

from sqlalchemy import and_, select

from xray_swagger.db.dao._base import DAOBase
from xray_swagger.db.models.defect import Defect, DefectCategory
from xray_swagger.db.models.product import InspectionSession, Product

# import sqlalchemy.orm as orm


if typing.TYPE_CHECKING:
    from xray_swagger.web.api.products.schema import InspectionSessionDTO, ProductDTO


__all__ = (
    "ProductDAO",
    "InspectionSessionDAO",
)


class ProductDAO(DAOBase):
    async def create(self, payload: "ProductDTO") -> Product:
        async with self.session.begin_nested():
            new_product = Product(**payload.model_dump(exclude_none=True))
            print(new_product)
            self.session.add(new_product)
        return new_product

    async def get(self, id: int) -> Product:
        raw = await self.session.execute(
            select(Product).where(
                Product.id == id,
            ),
        )
        return raw.scalar()

    async def get_all(self, offset: int = 0, limit: int = 20) -> list[Product]:
        raw = await self.session.execute(select(Product).offset(offset).limit(limit))
        return list(raw.scalars().fetchall())

    async def filter(self, name_query: str) -> list[Product]:
        raw = await self.session.execute(
            select(Product).where(
                Product.name.like(name_query),
            ),
        )
        return list(raw.scalars().fetchall())

    async def update(self, db_obj: Product, update_fields: "ProductDTO") -> Product:
        refined_update_fields = update_fields.model_dump(exclude_none=True)
        for k in refined_update_fields.keys():
            print(f"{type(db_obj).__name__}.{k} = {db_obj.__getattribute__(k)}")
        # UPDATE FIELDS
        async with self.session.begin_nested():
            print(f"=== UPDATE {type(db_obj).__name__}")
            for k, v in refined_update_fields.items():
                db_obj.__setattr__(k, v)

        for k in refined_update_fields.keys():
            print(f"{type(db_obj).__name__}.{k} = {db_obj.__getattribute__(k)}")
        return db_obj


class InspectionSessionDAO(DAOBase):
    async def create(self, payload: "InspectionSessionDTO"):
        async with self.session.begin_nested():
            new_isp_sess = InspectionSession(**payload.model_dump(exclude_none=True))
            print(new_isp_sess)
            self.session.add(new_isp_sess)
        return new_isp_sess

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

    async def get_all(
        self,
        product_id: int,
        offset: int = 0,
        limit: int = 20,
    ) -> list[InspectionSession]:
        raw = await self.session.execute(
            select(InspectionSession)
            .where(InspectionSession.product_id == product_id)
            .offset(offset)
            .limit(limit),
        )
        return list(raw.scalars().fetchall())

    async def filter(self, product_id: int) -> list[InspectionSession]:
        raw = await self.session.execute(
            select(InspectionSession).where(
                InspectionSession.product_id == product_id,
            ),
        )
        return list(raw.scalars().fetchall())


class DefectDAO(DAOBase):
    async def create(self, payload: "Defect"):
        async with self.session.begin_nested():
            new_isp_sess = Defect(**payload.model_dump(exclude_none=True))
            print(new_isp_sess)
            self.session.add(new_isp_sess)
        return new_isp_sess

    async def filter(
        self,
        product_id: int,
        isp_sess_id: int | None = None,
        defect_category: DefectCategory | None = None,
    ) -> list[Defect]:
        q = [Defect.product_id == product_id]
        if isp_sess_id:
            q.append(Defect.inspection_session_id == isp_sess_id)
        if defect_category:
            q.append(Defect.defect_category == defect_category)

        raw = await self.session.execute(
            select(Defect).filter(*q),
        )
        return list(raw.scalars().fetchall())
