from pydantic import BaseModel, ConfigDict


class SCategory(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)