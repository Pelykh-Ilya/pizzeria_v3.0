from pydantic import BaseModel, Field


class NewProductPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    description: str
    price: int
    units_in_stock: int = 0
    on_stop_list: bool = False


class GetProductPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
