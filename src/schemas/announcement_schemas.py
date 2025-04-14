import json
from typing import Optional

from pydantic import BaseModel, field_validator


class SAnnouncement(BaseModel):
    title: str
    description: str
    price: float = 1
    geo: Optional[str]
    status: bool = True
    type: Optional[str] = 'sale'
    category_id: Optional[int] = 1


    @field_validator('price', mode="before")
    def validate_price(cls, value):
        if value >= 0:
            return value
        else:
            raise ValueError("price must be more than 0")