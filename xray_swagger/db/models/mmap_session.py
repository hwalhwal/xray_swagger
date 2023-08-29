import typing

from sqlalchemy import UUID, Boolean, Column, DateTime, String

from xray_swagger.db.base import Base

if typing.TYPE_CHECKING:
    pass


class MmapSession(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True)
    image_s3_key = Column(String(512), nullable=False, unique=True)
    session_started_at = Column(DateTime, nullable=False)
    session_ended_at = Column(DateTime, nullable=True)
    is_preserved = Column(Boolean, nullable=False, default=True)
