from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class ProductDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    # inspection_sessions: URL
    # settings: URL

    creator_id: int | None = None
    last_editor_id: int | None = None

    created_at: datetime | None = None
    modified_at: datetime | None = None


class InspectionSessionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    # product = relationship("Product", back_populates="inspection_sessions")

    image_s3_key: str

    session_started_at: datetime | None = None
    session_ended_at: datetime | None = None

    system_error: str | None = None

    # defects = relationship()


class InspectionSessionCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int | None = None
    image_s3_key: str

    session_started_at: datetime = Field(default=datetime.utcnow())
    # Docker 내부에서 timezone 이슈 발생할것

    system_error: str | None = None

    @field_serializer("session_started_at")
    def serialize_session_started_at(self, value: datetime, _info):
        return value.utcnow()
