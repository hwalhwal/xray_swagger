"""
불량률 산정 알고리즘을 고려해야 함. 기간으로 조회할 수 있어야 함.
e.g.
SELECT COUNT(id) FROM ProductInspectionSession
WHERE
    id NOT IN Contaminant.product_inspection_session
    AND session_ended_at BETWEEN '2011/05/01' AND '2011/05/31';
"""

from tortoise import fields, models

from xray_swagger.db.models.mixins import TimestampMixin


class Product(TimestampMixin, models.Model):

    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255, null=False, unique=True)


class Product_Inspection_Session(models.Model):

    id = fields.UUIDField(pk=True)
    product = fields.ForeignKeyField(
        model_name="models.Product",
    )
    inspection_algorithm_ruleset = fields.ForeignKeyField(
        model_name="models.Inspection_Algorithm_Rule_Set",
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
