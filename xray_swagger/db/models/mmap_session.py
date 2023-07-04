from tortoise import fields, models


class Mmap_Session(models.Model):

    id = fields.IntField(pk=True)
    s3_key = fields.CharField(max_length=255, null=False, unique=True)
    session_started_at = fields.DatetimeField(null=False)
    session_ended_at = fields.DatetimeField(null=False)
    preservation = fields.BooleanField()
