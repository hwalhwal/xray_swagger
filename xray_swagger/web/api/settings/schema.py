from datetime import datetime
from typing import Any, Self

import fastjsonschema
from fastapi import HTTPException, status
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import JsonSchemaValue
from pydantic.types import AnyType
from pydantic_core import ErrorDetails

from xray_swagger.db.models.user import AuthLevel


class JsonSchemaValidateMixin:
    def validate_payload(
        param_value: Any,
        param_schema: JsonSchemaValue,
        **kwargs,
    ):
        json_validator = fastjsonschema.compile(param_schema)
        try:
            validated_value = json_validator(param_value)
            logger.debug(f"{validated_value}({type(validated_value)})")
            update_payload = dict(
                value=validated_value,
                **kwargs,
            )
        except fastjsonschema.exceptions.JsonSchemaValueException as err:
            logger.error(err.__dict__)
            detail = ErrorDetails(
                type="value_error",
                loc=err.name.split("."),
                msg=err.message,
                input=err.value,
                ctx=err.definition,
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=detail,
            ) from err
        return update_payload


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


class SettingsGlobalUpdateDTO(JsonSchemaValidateMixin, BaseModel):
    value: AnyType
    authlevel: AuthLevel | None = None

    last_editor_id: int | None = None
    modified_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def from_raw_value(
        cls,
        param_value: Any,
        param_schema: JsonSchemaValue,
        user_id: int,
    ) -> Self:
        payload = cls.validate_payload(
            param_value,
            param_schema,
            last_editor_id=user_id,
        )
        return cls(**payload)


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


class SettingsProductCreateDTO(JsonSchemaValidateMixin, BaseModel):
    product_id: int
    setting_param_name: str
    value: AnyType
    version: int = 1
    creator_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    last_editor_id: int
    modified_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def from_raw_value(
        cls,
        param_value: Any,
        param_schema: JsonSchemaValue,
        setting_param_name: str,
        product_id: int,
        user_id: int,
    ) -> Self:
        payload = cls.validate_payload(
            param_value,
            param_schema,
            product_id=product_id,
            setting_param_name=setting_param_name,
            creator_id=user_id,
            last_editor_id=user_id,
        )
        return cls(**payload)


class SettingsProductUpdateDTO(BaseModel):
    version: int
    value: AnyType
    last_editor_id: int | None = None
    modified_at: datetime = Field(default_factory=datetime.utcnow)


class SettingsProductChangelogDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    setting_param_name: str
    version: int
    patch: str

    last_editor_id: int | None = None
    created_at: datetime | None = None


class SettingsProductChangelogCreateDTO(BaseModel):
    product_id: int
    setting_param_name: str
    version: int
    patch: str

    last_editor_id: int
    created_at: datetime
