from enum import Enum

from tortoise import fields, models

from .mixins import TimestampMixin


class Algorithm_Name(str, Enum):

    ALAT_HP = "AlatHP"
    AL_003E = "Al003e"
    AL_DONG1 = "Aldong1"
    AL_007P2 = "Al007p2"
    AL_009 = "Al009"


class Inspection_Settings(models.Model):

    id = fields.IntField(pk=True)
    mode = fields.CharField(max_length=255)
    ng_behavior = fields.CharField(max_length=255)
    ng_image_store_policy = fields.CharField(max_length=255)
    image_trim = fields.CharField(max_length=255, null=True)
    product: fields.ForeignKeyRelation = fields.ForeignKeyField(
        model_name="models.Product",
        related_name="inspection_settings",
    )


class Inspection_Algorithm(models.Model):

    id = fields.IntField(pk=True)
    name = fields.CharEnumField(enum_type=Algorithm_Name, null=False)
    schema = fields.JSONField()  # JSON Schema로 파라미터별 이름, 설명, constraint 정의


class Inspection_Algorithm_Instance(TimestampMixin, models.Model):

    id = fields.IntField(pk=True)
    algorithm = fields.ForeignKeyField(model_name="models.Inspection_Algorithm")
    parameters = fields.JSONField()


class Inspection_Algorithm_Rule_Set(TimestampMixin, models.Model):

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=True)
    product: fields.ForeignKeyRelation = fields.ForeignKeyField(
        model_name="models.Product",
        related_name="inspection_algorithm_ruleset",
    )


class Rule_Set_Usage(TimestampMixin, models.Model):

    inspection_algorithm_ruleset = fields.ForeignKeyField(
        model_name="models.Inspection_Algorithm_Rule_Set",
        on_delete=fields.RESTRICT,
    )
    inspection_algorithm_instance = fields.ForeignKeyField(
        model_name="models.Inspection_Algorithm_Instance",
        on_delete=fields.RESTRICT,
    )
    order = fields.SmallIntField()
