from enum import Enum

from sqlalchemy import JSON, Column
from sqlalchemy import Enum as EnumField
from sqlalchemy import ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import relationship

from xray_swagger.db.base import Base
from xray_swagger.db.models.mixins import TimestampMixin


class Algorithm_Name(str, Enum):

    ALAT_HP = "AlatHP"
    AL_003E = "Al003e"
    AL_DONG1 = "Aldong1"
    AL_007P2 = "Al007p2"
    AL_009 = "Al009"


class Inspection_Setting(Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mode = Column(String(255))
    ng_behavior = Column(String(255))
    ng_image_store_policy = Column(String(255))
    image_trim = Column(String(255))
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", back_populates="inspection_setting")


class Inspection_Algorithm(Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(EnumField(Algorithm_Name), nullable=False)
    schema = Column(JSON, comment="JSON Schema로 파라미터별 이름, 설명, constraint 정의")


class Inspection_Algorithm_Instance(TimestampMixin, Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    algorithm_id = Column(Integer, ForeignKey("inspection_algorithm.id"))
    parameters = Column(JSON)


class Inspection_Algorithm_Rule_Set(TimestampMixin, Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    # product: fields.ForeignKeyRelation = fields.ForeignKeyField(
    #     model_name="models.Product",
    #     related_name="inspection_algorithm_ruleset",
    # )


class Rule_Set_Usage(TimestampMixin, Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    inspection_algorithm_ruleset_id = Column(
        Integer,
        ForeignKey("inspection_algorithm_rule_set.id", ondelete="RESTRICT"),
    )
    inspection_algorithm_instance_id = Column(
        Integer,
        ForeignKey("inspection_algorithm_instance.id", ondelete="RESTRICT"),
    )
    order = Column(SmallInteger)
