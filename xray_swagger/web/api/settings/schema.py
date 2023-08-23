from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import JsonSchemaValue
from pydantic.types import AnyType

from xray_swagger.db.models.user import AuthLevel


class _CreatedAt:
    created_at: datetime


class _ModifiedAt:
    modified_at: datetime


class _DeletedAt:
    _deleted_at: datetime | None = Field(default=None, alias="deleted_at")


class TimestampMixin(_CreatedAt, _ModifiedAt, _DeletedAt):
    ...


class _CreatorId:
    creator_id: int


class _LastEditorId:
    last_editor_id: int


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


class SettingsProductDTO(TimestampMixin, AuthorMixin, BaseModel):
    setting_param_name: str
    version: int
    value: AnyType
    product_id: int
