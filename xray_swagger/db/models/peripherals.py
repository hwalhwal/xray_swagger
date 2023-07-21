from peewee import *
from playhouse.postgres_ext import JSONField

from xray_swagger.db.models.product import Product


class Device_Info(Model):
    """Device Information.

    장치에 일반적으로 적용되는 사양을 제공.
    Fixture로 미리 적재해두고 특정 기능의 장치가 변경되었을 때 올바른 작동을 보장하도록 한다.
    """

    id = IntegerField(primary_key=True)
    product_name = CharField(max_length=255, null=False)
    product_code = CharField(max_length=255, null=False)
    model_series = CharField(max_length=255, null=False)
    manufacturer = CharField(max_length=255, null=False)
    specifications = JSONField()


class PeripheralDeviceBaseModel(Model):

    id = IntegerField(primary_key=True)
    serial_number = CharField(max_length=255, null=False, unique=True)
    device_info = ForeignKeyField(model=Device_Info)
    settings = JSONField()

    class Meta:
        abstract = True


class Conveyor(PeripheralDeviceBaseModel):

    product = ForeignKeyField(
        model_name=Product,
        backref="conveyor_settings",
        null=True,
        lazy_load=True,
    )


class Rejector(PeripheralDeviceBaseModel):
    product = ForeignKeyField(
        model_name=Product,
        backref="rejector_settings",
        null=True,
        lazy_load=True,
    )


class Xray_Emitter(PeripheralDeviceBaseModel):

    product = ForeignKeyField(
        model_name=Product,
        backref="xray_emitter_settings",
        null=True,
        lazy_load=True,
    )
    max_scan_range = IntegerField(description="in mm")
    max_scan_velocity = IntegerField(description="in cm/min")
    max_voltage = DecimalField(
        max_digits=10,
        decimal_places=4,
        description="in kV",
    )
    max_current = DecimalField(
        max_digits=10,
        decimal_places=4,
        description="in mA",
    )

    class Meta:
        table_description = "Hello"


class Xray_Detector(PeripheralDeviceBaseModel):

    product = ForeignKeyField(
        model_name=Product,
        backref="xray_detector_settings",
        null=True,
        lazy_load=True,
    )


class Metal_Detector(PeripheralDeviceBaseModel):

    product = ForeignKeyField(
        model_name=Product,
        backref="metal_detector_settings",
        null=True,
        lazy_load=True,
    )
