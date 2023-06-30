from enum import Enum

from tortoise import fields, models

from .mixins import TimestampMixin


class Algorithm_Name(str, Enum):

    ALAT_HP = "AlatHP"
    AL_003E = "Al003e"
    AL_DONG1 = "Aldong1"
    AL_007P2 = "Al007p2"
    AL_009 = "Al009"


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
