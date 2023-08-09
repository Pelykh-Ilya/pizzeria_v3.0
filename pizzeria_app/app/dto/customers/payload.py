from pydantic import BaseModel, Field


class NewCustomerPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    address: str = "pickup"
    phone: str = Field(..., min_length=1, max_length=32)


class EditCustomerByPhonePayload(BaseModel):
    phone: str = Field(..., min_length=1, max_length=32)
