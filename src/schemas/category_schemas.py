from pydantic import BaseModel


class SCategory(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True