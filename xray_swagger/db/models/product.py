"""
불량률 산정 알고리즘을 고려해야 함. 기간으로 조회할 수 있어야 함.
e.g.
SELECT COUNT(id) FROM ProductInspectionSession
WHERE
    id NOT IN Contaminant.product_inspection_session
    AND session_ended_at BETWEEN '2011/05/01' AND '2011/05/31';
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from xray_swagger.db.base import Base
from xray_swagger.db.models.defect import Defect
from xray_swagger.db.models.mixins import AuthorMixin, TimestampMixin


class Product(TimestampMixin, AuthorMixin, Base):
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    inspection_sessions = relationship("InspectionSession")
    settings = relationship("SettingsProduct", back_populates="product")


class InspectionSession(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product", back_populates="inspection_sessions")

    image_s3_key = Column(String(512), nullable=False, unique=True)

    session_started_at = Column(DateTime, nullable=False)
    session_ended_at = Column(DateTime, nullable=True)

    system_error = Column(Text, nullable=True)

    defects = relationship(
        Defect,
        back_populates="inspection_session",
    )
