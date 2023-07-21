from datetime import datetime

from peewee import DateTimeField


class TimestampMixin:
    created_at = DateTimeField(null=True, default=datetime.now)
    modified_at = DateTimeField(
        null=True,
        default=datetime.now,
    )  # on update CURRENT_TIMESTAMP
    deleted_at = DateTimeField(null=True)
