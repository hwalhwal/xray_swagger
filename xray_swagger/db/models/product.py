"""
불량률 산정 알고리즘을 고려해야 함. 기간으로 조회할 수 있어야 함.
e.g.
SELECT COUNT(id) FROM ProductInspectionSession
WHERE
    id NOT IN Contaminant.product_inspection_session
    AND session_ended_at BETWEEN '2011/05/01' AND '2011/05/31';
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from xray_swagger.db.base import Base
from xray_swagger.db.models.mixins import TimestampMixin


class Product(TimestampMixin, Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    product_inspection_sessions = relationship(
        "Product_Inspection_Session",
        back_populates="product",
    )

    inspection_algorithm_ruleset = relationship(
        "Inspection_Algorithm_Rule_Set",
        back_populates="product",
        uselist=False,
    )  # 1:1
    inspection_setting = relationship(
        "Inspection_Setting",
        back_populates="product",
        uselist=False,
    )
    conveyor_setting = relationship("Conveyor", back_populates="product", uselist=False)
    rejector_setting = relationship("Rejector", back_populates="product", uselist=False)
    xray_emitter_setting = relationship(
        "Xray_Emitter",
        back_populates="product",
        uselist=False,
    )
    xray_detector_setting = relationship(
        "Xray_Detector",
        back_populates="product",
        uselist=False,
    )
    metal_detector_setting = relationship(
        "Metal_Detector",
        back_populates="product",
        uselist=False,
    )


class Product_Inspection_Session(Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product", back_populates="product_inspection_sessions")
    image_s3_key = Column(String(255), nullable=False, unique=True)

    session_started_at = Column(DateTime, nullable=False)
    session_ended_at = Column(DateTime, nullable=False)

    # TODO
    start_mmap_session = relationship("Mmap_Session")
    start_mmap_session_ptr = Column(Integer, nullable=False)

    end_mmap_session = relationship("Mmap_Session")
    end_mmap_session_ptr = Column(Integer, nullable=False)

    system_error = Column(String(1024), nullable=True)

    contaminants = relationship(
        "Contaminant",
        back_populates="product_inspection_session",
    )
