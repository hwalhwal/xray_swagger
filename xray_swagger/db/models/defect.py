import enum
import typing

from sqlalchemy import JSON, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from xray_swagger.db.base import Base

if typing.TYPE_CHECKING:
    from .product import InspectionSession


class DefectCategory(enum.Enum):
    CONTAMINANT = 1
    METAL = 2
    MISSING_PRODUCT = 4
    DAMAGED = 8


class Defect(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    defect_category = Column(Enum(DefectCategory), nullable=False)
    inspection_module = Column(String(128), nullable=False)
    coordinates = Column(JSON, nullable=True)
    product_id = Column(
        Integer,
        ForeignKey("product.id"),
        nullable=False,
    )
    inspection_session_id = Column(
        Integer,
        ForeignKey("inspection_session.id"),
        nullable=False,
    )
    inspection_session: Mapped["InspectionSession"] = relationship(
        back_populates="defects",
    )
    # TODO: Index("idx_product_param", product_id, inspection_session_id, defect_category)
