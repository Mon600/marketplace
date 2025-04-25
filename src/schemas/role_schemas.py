from pydantic import BaseModel, ConfigDict


class SRole(BaseModel):
    id: int
    role: str

    model_config = ConfigDict(from_attributes=True)