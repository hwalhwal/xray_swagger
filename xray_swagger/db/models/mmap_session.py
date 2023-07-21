from peewee import *


class Mmap_Session(Model):

    id = IntegerField(primary_key=True)
    s3_key = CharField(max_length=255, null=False, unique=True)
    session_started_at = DateTimeField(null=False)
    session_ended_at = DateTimeField(null=False)
    preservation = BooleanField()
