from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from pydantic.types import AnyType, conlist

from xray_swagger.db.models.defect import DefectCategory


class ProductDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

    # inspection_sessions: URL
    # settings: URL

    creator_id: int | None = None
    last_editor_id: int | None = None

    created_at: datetime | None = None
    modified_at: datetime | None = None


class ProductCreateDTO(BaseModel):
    name: str

    creator_id: int | None = None
    last_editor_id: int | None = None

    created_at: datetime | None = None
    modified_at: datetime | None = None


class InspectionSessionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    # product: ProductDTO | None = None

    image_s3_key: str

    session_started_at: datetime | None = None
    session_ended_at: datetime | None = None

    system_error: str | None = None

    # defects = relationship()


class InspectionSessionCreateDTO(BaseModel):
    product_id: int | None = None
    image_s3_key: str

    session_started_at: datetime = Field(default_factory=datetime.utcnow)
    # Docker 내부에서 timezone 이슈 발생할것

    system_error: str | None = None

    @field_serializer("session_started_at")
    def serialize_session_started_at(self, value: datetime, _info):
        return value.replace(tzinfo=None)


class InspectionSessionUpdateDTO(BaseModel):
    image_s3_key: str | None = None

    session_started_at: datetime | None = None
    session_ended_at: datetime | None = None

    system_error: str | None = None


class DefectDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    defect_category: DefectCategory
    inspection_module: str
    coordinates: AnyType
    product_id: int
    inspection_session_id: int


class DefectCreateDTO(BaseModel):
    defect_category: DefectCategory
    inspection_module: str | None = None
    coordinates: conlist(int, min_length=4, max_length=4)
    inspection_session_id: int


class DefectUpdateDTO(BaseModel):
    defect_category: DefectCategory | None = None
    inspection_module: str | None = None
    coordinates: conlist(int, min_length=4, max_length=4) | None = None
    inspection_session_id: int | None = None
