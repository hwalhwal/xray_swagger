from datetime import datetime, timedelta
from typing import Annotated
from uuid import uuid4

from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    SerializerFunctionWrapHandler,
    WrapSerializer,
)


def dt_to_utcnow(dt: datetime, nxt: SerializerFunctionWrapHandler) -> datetime:
    ohne_tz = dt.replace(tzinfo=None)
    return nxt(ohne_tz)


UTCDatetime = Annotated[datetime, WrapSerializer(dt_to_utcnow)]
# TODO: Used This in all schemas[DTO]


def laggedutc() -> datetime:
    now = datetime.utcnow()
    return now + timedelta(minutes=5)


class MmapSessionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID4
    image_s3_key: str
    session_started_at: datetime | None = None
    session_ended_at: datetime | None = None
    is_preserved: bool


class MmapSessionCreateDTO(BaseModel):
    uuid: UUID4 = Field(default_factory=uuid4)
    image_s3_key: str
    session_started_at: UTCDatetime | None = Field(default_factory=datetime.utcnow)
    session_ended_at: UTCDatetime | None = Field(default_factory=laggedutc)


class MmapSessionUpdateDTO(BaseModel):
    image_s3_key: str | None = None
    session_started_at: datetime | None = None
    session_ended_at: datetime | None = None
    is_preserved: bool | None = None
