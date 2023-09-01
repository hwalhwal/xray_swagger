from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, SecretStr, field_serializer
from pydantic_extra_types.phone_numbers import PhoneNumber

from xray_swagger.db.models.user import AuthLevel


class UserModelDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: SecretStr

    fullname: str
    phone_number: Optional[PhoneNumber] = None
    company: Optional[str] = None
    job_title: Optional[str] = None

    joined_at: datetime
    last_sign_in_at: Optional[datetime] = None
    # last_sign_in_at: datetime
    deleted_at: Optional[datetime] = None

    authlevel: AuthLevel


class UserCreateDTO(BaseModel):
    """Schema for User creation"""

    model_config = ConfigDict(from_attributes=True)

    username: str
    password: SecretStr
    fullname: str
    phone_number: Optional[PhoneNumber] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    authlevel: Optional[AuthLevel] = AuthLevel.OPERATOR

    @field_serializer("password")
    def serialize_password(self, password: SecretStr, _info) -> str:
        return password.get_secret_value()


class UserUpdateDTO(BaseModel):
    fullname: Optional[str] = None
    phone_number: Optional[PhoneNumber] = None
    authlevel: Optional[AuthLevel] = None
    job_title: Optional[str] = None
