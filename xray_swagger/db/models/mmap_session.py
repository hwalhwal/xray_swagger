from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from xray_swagger.db.base import Base


class MmapSession(Base):

    uuid = Column(UUID, primary_key=True)
    image_s3_key = Column(String(512), nullable=False, unique=True)
    session_started_at = Column(DateTime, nullable=False)
    session_ended_at = Column(DateTime, nullable=True)
    is_preserved = Column(Boolean, nullable=False, default=True)


class MmapPointer(Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    inspection_session_id = Column(ForeignKey("inspection_session.id"), nullable=False)

    start_mmap_session_uuid = Column(
        UUID,
        ForeignKey("mmap_session.uuid"),
        nullable=False,
    )
    start_mmap_session = relationship(
        "MmapSession",
        foreign_keys=[start_mmap_session_uuid],
    )
    start_mmap_session_ptr = Column(Integer, nullable=False)

    end_mmap_session_uuid = Column(
        UUID,
        ForeignKey("mmap_session.uuid"),
        nullable=True,
    )
    end_mmap_session = relationship(
        "MmapSession",
        foreign_keys=[end_mmap_session_uuid],
    )
    end_mmap_session_ptr = Column(Integer, nullable=False)
