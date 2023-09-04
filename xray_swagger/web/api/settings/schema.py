from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import JsonSchemaValue
from pydantic.types import AnyType

from xray_swagger.db.models.user import AuthLevel


class SettingsProductParameterDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    setting_param_name: str
    authlevel: AuthLevel
    json_schema: JsonSchemaValue


class SettingsGlobalDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    setting_param_name: str
    authlevel: AuthLevel
    json_schema: JsonSchemaValue
    value: AnyType

    last_editor_id: int | None = None
    modified_at: datetime | None = None


class SettingsGlobalUpdateDTO(BaseModel):
    value: AnyType
    authlevel: AuthLevel | None = None

    last_editor_id: int | None = None
    modified_at: datetime | None = None


class SettingsProductDTO(BaseModel):
    id: int
    product_id: int
    setting_param_name: str
    version: int
    value: AnyType

    creator_id: int | None = None
    created_at: datetime | None = None

    last_editor_id: int | None = None
    modified_at: datetime | None = None

    deleted_at: datetime | None = Field(default=None, alias="deleted_at")


class SettingsProductCreateDTO(BaseModel):
    product_id: int
    setting_param_name: str
    version: int
    value: AnyType


class SettingsProductUpdateDTO(BaseModel):
    version: int
    value: AnyType
    last_editor_id: int | None = None
