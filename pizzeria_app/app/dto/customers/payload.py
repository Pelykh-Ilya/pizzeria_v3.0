import re

from pydantic import BaseModel, Field, field_validator


class NewCustomerPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    address: str | None = None
    phone: str = Field(..., min_length=1, max_length=32)

    @field_validator("phone")
    def validate_phone(cls, value: str):
        phone_pattern = re.compile(r'^\+380\d{9}$')

        if not phone_pattern.match(value):
            raise ValueError("Incorrect phone number")
        return value


class EditCustomerPayload(BaseModel):
    name: str = Field(None, min_length=1, max_length=128)
    address: str | None = None
    is_active: bool | None = None
    phone: str | None = Field(None, min_length=1, max_length=32)

    @field_validator("phone")
    def validate_phone(cls, value: str | None):
        if not value:
            return
        phone_pattern = re.compile(r'^\+380\d{9}$')

        if not phone_pattern.match(value):
            raise ValueError("Incorrect phone number")
        return value
