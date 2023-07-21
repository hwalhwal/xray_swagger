from peewee import *


class DummyModel(Model):
    """Model for demo purpose."""

    id = IntegerField(primary_key=True)
    name = CharField(max_length=200)  # noqa: WPS432

    def __str__(self) -> str:
        return self.name
