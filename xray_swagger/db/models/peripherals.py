from sqlalchemy import DECIMAL, JSON, Column, ForeignKey, Integer, String

from xray_swagger.db.base import Base


class Device_Info(Base):
    """Device Information.

    장치에 일반적으로 적용되는 사양을 제공.
    Fixture로 미리 적재해두고 특정 기능의 장치가 변경되었을 때 올바른 작동을 보장하도록 한다.
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    product_code = Column(String(255), nullable=False)
    model_series = Column(String(255), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    specifications = Column(JSON)


class PeripheralDeviceBaseModel:

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    serial_number = Column(String(255), nullable=False, unique=True)
    device_info_id = Column(Integer, ForeignKey("device_info.id"))
    settings = Column(JSON)


# class Conveyor(PeripheralDeviceBaseModel):

#     product: fields.ForeignKeyNullableRelation = fields.ForeignKeyField(
#         model_name="models.Product",
#         related_name="conveyor_settings",
#         null=True,
#     )


# class Rejector(PeripheralDeviceBaseModel):
#     product: fields.ForeignKeyNullableRelation = fields.ForeignKeyField(
#         model_name="models.Product",
#         related_name="rejector_settings",
#         null=True,
#     )


class Xray_Emitter(PeripheralDeviceBaseModel, Base):

    max_scan_range = Column(Integer, comment="in mm")
    max_scan_velocity = Column(Integer, comment="in cm/min")
    max_voltage = Column(DECIMAL(precision=10, scale=4), comment="in kV")
    max_current = Column(DECIMAL(precision=10, scale=4), comment="in mA")


# class Xray_Detector(PeripheralDeviceBaseModel):

#     product: fields.ForeignKeyNullableRelation = fields.ForeignKeyField(
#         model_name="models.Product",
#         related_name="xray_detector_settings",
#         null=True,
#     )


# class Metal_Detector(PeripheralDeviceBaseModel):

#     product: fields.ForeignKeyNullableRelation = fields.ForeignKeyField(
#         model_name="models.Product",
#         related_name="metal_detector_settings",
#         null=True,
#     )
