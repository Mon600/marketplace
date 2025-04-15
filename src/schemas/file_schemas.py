from pydantic import BaseModel


class SFile(BaseModel):
    announcement_id: int = ''
    url: str = ''
    type: str =''

class SFileGet(SFile):
    id: int