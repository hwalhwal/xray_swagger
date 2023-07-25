from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from xray_swagger.db.base import Base


class User(Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    firstname = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    phone_number = Column(String(128), nullable=False)
    job_title = Column(String(128), nullable=False)

    date_joined = Column(DateTime, default=func.now())
    last_signin = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime, default=None)

    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    def __str__(self) -> str:
        return self.name
