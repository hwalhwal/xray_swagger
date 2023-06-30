from tortoise import fields, models


class User(models.Model):

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=200, null=False, unique=True)
    firstname = fields.CharField(max_length=128, null=False)
    lastname = fields.CharField(max_length=128, null=False)
    password = fields.CharField(max_length=128, null=False)
    phone_number = fields.CharField(max_length=128, null=False)
    job_title = fields.CharField(max_length=128, null=False)

    date_joined = fields.DatetimeField(auto_now_add=True)
    last_signin = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(default=None)

    is_staff = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
