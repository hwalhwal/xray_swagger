"""
불량률 산정 알고리즘을 고려해야 함. 기간으로 조회할 수 있어야 함.
e.g.
SELECT COUNT(id) FROM ProductInspectionSession
WHERE
    id NOT IN Contaminant.product_inspection_session
    AND session_ended_at BETWEEN '2011/05/01' AND '2011/05/31';
"""
from peewee import *

from xray_swagger.db.models.mixins import TimestampMixin
from xray_swagger.db.models.mmap_session import Mmap_Session


class Product(TimestampMixin, Model):

    id = IntegerField(primary_key=True)
    name = CharField(max_length=255, null=False, unique=True)
    # inspection_algorithm_ruleset = fields.ReverseRelation[
    #     "Inspection_Algorithm_Rule_Set"
    # ]
    # inspection_settings: fields.ReverseRelation["Inspection_Settings"]
    # conveyor_settings: fields.ReverseRelation["Conveyor"]
    # rejector_settings: fields.ReverseRelation["Rejector"]
    # xray_emitter_settings: fields.ReverseRelation["Xray_Emitter"]
    # xray_detector_settings: fields.ReverseRelation["Xray_Detector"]
    # metal_detector_settings: fields.ReverseRelation["Metal_Detector"]


class Product_Inspection_Session(Model):

    id = IntegerField(primary_key=True)
    product = ForeignKeyField(
        model_name=Product,
        backref="product_inspections_sessions",
        lazy_load=True,
    )
    image_s3_key = CharField(max_length=255, null=False, unique=True)
    session_started_at = DateTimeField(null=False)
    session_ended_at = DateTimeField(null=False)
    start_mmap_session = ForeignKeyField(
        model_name=Mmap_Session,
        backref="product_start",
        lazy_load=True,
    )
    start_mmap_session_ptr = IntegerField(null=False)
    end_mmap_session = ForeignKeyField(
        model_name=Mmap_Session,
        related_name="product_end",
        lazy_load=True,
    )
    end_mmap_session_ptr = IntegerField(null=False)
    system_error = TextField(null=True)
