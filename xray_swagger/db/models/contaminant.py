from enum import Enum, auto

from sqlalchemy import JSON, Column
from sqlalchemy import Enum as EnumField
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship

from xray_swagger.db.base import Base


class Contaminant_Category(Enum):
    METAL = auto()
    NON_FERROUS_METAL = auto()
    GLASS = auto()
    BONE = auto()
    PVC = auto()
    TFE = auto()
    CERAMIC_CONCRETE = auto()
    MISSING_PRODUCT = auto()


class Shape(Enum):
    CIRCLE = auto()
    ELLIPSE = auto()
    OVAL = auto()
    RECTANGLE = auto()
    POLYGON = auto()


class Contaminant(Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(EnumField(Contaminant_Category), comment="이물의 카테고리를 지정한다")
    shape = Column(EnumField(Shape), comment="이물 표시 영역의 모양")
    coordinates = Column(JSON)
    product_inspection_session_id = Column(
        Integer,
        ForeignKey("product_inspection_session.id"),
        nullable=False,
    )
    product_inspection_session = relationship(
        "Product_Inspection_Session",
        back_populates="contaminants",
    )
