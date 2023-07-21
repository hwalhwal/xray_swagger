from enum import Enum, auto

from peewee import *
from playhouse.postgres_ext import JSONField

from xray_swagger.db.database import db
from xray_swagger.db.models.product import Product_Inspection_Session


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


class Contaminant(Model):

    id = IntegerField(primary_key=True)

    category = CharField(
        max_length=64,
        description="이물의 카테고리를 지정한다",
    )
    shape = CharField(max_length=64, description="이물 표시 영역의 모양")
    coordinates = JSONField()
    product_inspection_session = ForeignKeyField(
        model=Product_Inspection_Session,
        backref="product_contaminants",
    )

    class Meta:
        database = db
