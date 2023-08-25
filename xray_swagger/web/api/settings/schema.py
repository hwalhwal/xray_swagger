from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import JsonSchemaValue
from pydantic.types import AnyType

from xray_swagger.db.models.user import AuthLevel


class _CreatedAt(BaseModel):
    created_at: datetime | None = None


class _ModifiedAt(BaseModel):
    modified_at: datetime | None = None


class _DeletedAt(BaseModel):
    deleted_at: datetime | None = Field(default=None, alias="deleted_at")


class TimestampMixin(_CreatedAt, _ModifiedAt, _DeletedAt):
    ...


class _CreatorId(BaseModel):
    creator_id: int | None = None


class _LastEditorId(BaseModel):
    last_editor_id: int | None = None


class AuthorMixin(_CreatorId, _LastEditorId):
    ...


class SettingsProductParameterDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    setting_param_name: str
    authlevel: AuthLevel
    json_schema: JsonSchemaValue


class SettingsGlobalDTO(_ModifiedAt, _LastEditorId, BaseModel):
    model_config = ConfigDict(from_attributes=True)

    setting_param_name: str
    authlevel: AuthLevel
    json_schema: JsonSchemaValue
    value: AnyType


class SettingsProductDTO(BaseModel):
    product_id: int
    setting_param_name: str
    version: int
    value: AnyType


class SettingsProductUpdateDTO(BaseModel):
    version: int
    value: AnyType
    last_editor_id: int | None = None


class FullSettingsProductDTO(TimestampMixin, AuthorMixin, SettingsProductDTO):
    ...
