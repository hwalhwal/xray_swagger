from sqlalchemy import UUID, Boolean, Column, DateTime, String

from xray_swagger.db.base import Base


class Mmap_Session(Base):

    uuid = Column(UUID, primary_key=True)
    s3_key = Column(String(512), nullable=False, unique=True)
    session_started_at = Column(DateTime, nullable=False)
    session_ended_at = Column(DateTime, nullable=False)
    preservation = Column(Boolean)
