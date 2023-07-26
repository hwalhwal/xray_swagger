import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func

from xray_swagger.db.base import Base


class AuthLevel(enum.Enum):
    OPERATOR = 0
    STAFF = 1
    ENGINEER = 2


class User(Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    fullname = Column(String(64), nullable=False)
    phone_number = Column(String(128), nullable=True)
    company = Column(String(128), nullable=True)
    job_title = Column(String(128), nullable=True)

    joined_at = Column(DateTime, default=func.now())
    last_sign_in_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime, default=None)

    authlevel = Column(Enum(AuthLevel), default=AuthLevel.OPERATOR)

    def __str__(self) -> str:
        return self.name
