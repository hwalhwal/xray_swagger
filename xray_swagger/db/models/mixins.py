from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func


class TimestampMixin:

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )
    modified_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp(),
    )
    deleted_at = Column(DateTime, nullable=True)


class AuthorMixin:

    creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    last_editor_id = Column(Integer, ForeignKey("user.id"), nullable=False)
