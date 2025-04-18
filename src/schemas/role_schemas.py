from pydantic import BaseModel


class SRole(BaseModel):
    id: int
    role: str

    class Config:
        from_attributes = True