from enum import Enum, auto

from tortoise import fields, models


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


class Contaminant(models.Model):

    id = fields.IntField(pk=True)
    category = fields.IntEnumField(
        enum_type=Contaminant_Category,
        description="이물의 카테고리를 지정한다",
    )
    shape = fields.IntEnumField(enum_type=Shape, description="이물 표시 영역의 모양")
    coordinates = fields.JSONField()
    product_inspection_session = fields.ForeignKeyField(
        model_name="models.Product_Inspection_Session",
        related_name="product_contaminants",
    )
