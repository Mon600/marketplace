from pydantic import BaseModel, ConfigDict


class SFile(BaseModel):
    announcement_id: int = ''
    url: str = ''
    type: str =''

class SFileGet(SFile):
    id: int

    model_config = ConfigDict(from_attributes=True)