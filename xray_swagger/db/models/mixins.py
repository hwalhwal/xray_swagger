from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func


class _CreatedAt:
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )


class _ModifiedAt:
    modified_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp(),
    )


class _DeletedAt:
    deleted_at = Column(DateTime, nullable=True)


class TimestampMixin(_CreatedAt, _ModifiedAt, _DeletedAt):
    ...


class _CreatorId:
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)


class _LastEditorId:
    last_editor_id = Column(Integer, ForeignKey("user.id"), nullable=False)


class AuthorMixin(_CreatorId, _LastEditorId):
    ...
