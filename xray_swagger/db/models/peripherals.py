from sqlalchemy import JSON, Column, Integer, String

from xray_swagger.db.base import Base


class Device(Base):
    """Device Information.

    장치에 일반적으로 적용되는 사양을 제공.
    Fixture로 미리 적재해두고 특정 기능의 장치가 변경되었을 때 올바른 작동을 보장하도록 한다.
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    model_series = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    specifications = Column(JSON)
