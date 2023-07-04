from tortoise import fields, models


class Device_Info(models.Model):
    """Device Information.

    장치에 일반적으로 적용되는 사양을 제공.
    Fixture로 미리 적재해두고 특정 기능의 장치가 변경되었을 때 올바른 작동을 보장하도록 한다.
    """

    id = fields.IntField(pk=True)
    product_name = fields.CharField(max_length=255, null=False)
    product_code = fields.CharField(max_length=255, null=False)
    model_series = fields.CharField(max_length=255, null=False)
    manufacturer = fields.CharField(max_length=255, null=False)
    specifications = fields.JSONField()


class PeripheralDeviceBaseModel(models.Model):

    id = fields.IntField(pk=True)
    serial_number = fields.CharField(max_length=255, null=False, unique=True)
    device_info = fields.ForeignKeyField(
        model_name="models.Device_Info",
    )
    settings = fields.JSONField()

    class Meta:
        abstract = True


class Conveyor(PeripheralDeviceBaseModel):

    product: fields.ForeignKeyNullableRelation = fields.ForeignKeyField(
        model_name="models.Product",
        related_name="conveyor_settings",
        null=True,
    )


class Rejector(PeripheralDeviceBaseModel):
    product: fields.ForeignKeyNullableRelation = fields.ForeignKeyField(
        model_name="models.Product",
        related_name="rejector_settings",
        null=True,
    )


class Xray_Emitter(PeripheralDeviceBaseModel):

    product: fields.ForeignKeyNullableRelation = fields.ForeignKeyField(
        model_name="models.Product",
        related_name="xray_emitter_settings",
        null=True,
    )
    max_scan_range = fields.IntField(description="in mm")
    max_scan_velocity = fields.IntField(description="in cm/min")
    max_voltage = fields.DecimalField(
        max_digits=10,
        decimal_places=4,
        description="in kV",
    )
    max_current = fields.DecimalField(
        max_digits=10,
        decimal_places=4,
        description="in mA",
    )

    class Meta:
        table_description = "Hello"


class Xray_Detector(PeripheralDeviceBaseModel):

    product: fields.ForeignKeyNullableRelation = fields.ForeignKeyField(
        model_name="models.Product",
        related_name="xray_detector_settings",
        null=True,
    )


class Metal_Detector(PeripheralDeviceBaseModel):

    product: fields.ForeignKeyNullableRelation = fields.ForeignKeyField(
        model_name="models.Product",
        related_name="metal_detector_settings",
        null=True,
    )
