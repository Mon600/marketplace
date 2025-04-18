from typing import Optional

from pydantic import BaseModel, field_validator

from schemas.role_schemas import SRole


class SChange(BaseModel):
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    phone: Optional[str] = ''

    @field_validator("phone", mode="before")
    def validate_phone(cls, value):
        if value == '' or value is None:
            return value
        if not value.isdigit():
            raise ValueError("Phone number must be only digits")
        elif len(value) < 11:
            raise ValueError("Phone number must be at least 11 digits")
        elif (not value.startswith("7")) and (not value.startswith("8")):
            raise ValueError("Phone number must start with 7 or 8")
        else:
            return value


class SRegister(BaseModel):
    yandex_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: str


class SUser(SRegister):
    phone: Optional[str]
    roles_rel: Optional[SRole]

    class Config:
        from_attributes = True


