"""
불량률 산정 알고리즘을 고려해야 함. 기간으로 조회할 수 있어야 함.
e.g.
SELECT COUNT(id) FROM ProductInspectionSession
WHERE
    id NOT IN Contaminant.product_inspection_session
    AND session_ended_at BETWEEN '2011/05/01' AND '2011/05/31';
"""

from tortoise import fields, models

from xray_swagger.db.models.inspection import Inspection_Settings
from xray_swagger.db.models.mixins import TimestampMixin
from xray_swagger.db.models.peripherals import (
    Conveyor,
    Metal_Detector,
    Rejector,
    Xray_Detector,
    Xray_Emitter,
)


class Product(TimestampMixin, models.Model):

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False, unique=True)
    inspection_algorithm_ruleset = fields.ReverseRelation[
        "Inspection_Algorithm_Rule_Set"
    ]
    inspection_settings: fields.ReverseRelation["Inspection_Settings"]
    conveyor_settings: fields.ReverseRelation["Conveyor"]
    rejector_settings: fields.ReverseRelation["Rejector"]
    xray_emitter_settings: fields.ReverseRelation["Xray_Emitter"]
    xray_detector_settings: fields.ReverseRelation["Xray_Detector"]
    metal_detector_settings: fields.ReverseRelation["Metal_Detector"]


class Product_Inspection_Session(models.Model):

    id = fields.IntField(pk=True)
    product = fields.ForeignKeyField(
        model_name="models.Product",
    )
    image_s3_key = fields.CharField(max_length=255, null=False, unique=True)
    session_started_at = fields.DatetimeField(null=False)
    session_ended_at = fields.DatetimeField(null=False)
    start_mmap_session = fields.ForeignKeyField(
        model_name="models.Mmap_Session",
        related_name="product_start",
    )
    start_mmap_session_ptr = fields.IntField(null=False)
    end_mmap_session = fields.ForeignKeyField(
        model_name="models.Mmap_Session",
        related_name="product_end",
    )
    end_mmap_session_ptr = fields.IntField(null=False)
    system_error = fields.TextField(null=True)
