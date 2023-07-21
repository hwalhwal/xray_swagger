from peewee import *


class User(Model):

    id = IntegerField(primary_key=True)
    username = CharField(max_length=200, null=False, unique=True)
    firstname = CharField(max_length=128, null=False)
    lastname = CharField(max_length=128, null=False)
    password = CharField(max_length=128, null=False)
    phone_number = CharField(max_length=128, null=False)
    job_title = CharField(max_length=128, null=False)

    date_joined = DateTimeField(auto_now_add=True)
    last_signin = DateTimeField(auto_now=True)
    deleted_at = DateTimeField(default=None)

    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
