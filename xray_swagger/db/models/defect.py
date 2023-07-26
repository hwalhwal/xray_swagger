import enum

from sqlalchemy import JSON, Column, Enum, ForeignKey, Integer, String

from xray_swagger.db.base import Base


class DefectCategory(enum.StrEnum):
    CONTAMINANT = 1
    METAL = 2
    MISSING_PRODUCT = 4
    DAMAGED = 8


class Defect(Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    defect_category = Column(Enum(DefectCategory), nullable=False)
    inspection_module = Column(String(128), nullable=False)
    coordinates = Column(JSON, nullable=True)
    inspection_session_id = Column(
        Integer,
        ForeignKey("inspection_session.id"),
        nullable=False,
    )
