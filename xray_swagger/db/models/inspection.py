from enum import Enum

from peewee import *
from playhouse.postgres_ext import JSONField

from xray_swagger.db.models.mixins import TimestampMixin
from xray_swagger.db.models.product import Product


class Algorithm_Name(str, Enum):

    ALAT_HP = "AlatHP"
    AL_003E = "Al003e"
    AL_DONG1 = "Aldong1"
    AL_007P2 = "Al007p2"
    AL_009 = "Al009"


class Inspection_Settings(Model):

    id = IntegerField(primary_key=True)
    mode = CharField(max_length=255)
    ng_behavior = CharField(max_length=255)
    ng_image_store_policy = CharField(max_length=255)
    image_trim = CharField(max_length=255, null=True)
    product = ForeignKeyField(
        model=Product,
        backref="inspection_settings",
    )


class Inspection_Algorithm(Model):

    id = IntegerField(primary_key=True)
    # name = fields.CharEnumField(enum_type=Algorithm_Name, null=False)
    name = CharField(max_length=256)
    schema = JSONField()  # JSON Schema로 파라미터별 이름, 설명, constraint 정의


class Inspection_Algorithm_Instance(TimestampMixin, Model):

    id = IntegerField(primary_key=True)
    algorithm = ForeignKeyField(model=Inspection_Algorithm)
    parameters = JSONField()


class Inspection_Algorithm_Rule_Set(TimestampMixin, Model):

    id = IntegerField(primary_key=True)
    name = CharField(max_length=255, null=True)
    product = ForeignKeyField(
        model=Product,
        backref="inspection_algorithm_ruleset",
    )


class Rule_Set_Usage(TimestampMixin, Model):

    inspection_algorithm_ruleset = ForeignKeyField(
        model=Inspection_Algorithm_Rule_Set,
        on_delete="RESTRICT",
    )
    inspection_algorithm_instance = ForeignKeyField(
        model=Inspection_Algorithm_Instance,
        on_delete="RESTRICT",
    )
    order = SmallIntegerField()
