import json
from typing import Optional, Any, List, Annotated

from fastapi.params import Depends
from pydantic import BaseModel, field_validator, model_validator, Field, ConfigDict

from schemas.file_schemas import SFileGet
from schemas.user_schemas import SUser


class SAnnouncement(BaseModel):
    title: str = ""
    description: str = ""
    price: float = 1
    geo: Optional[str] = ""
    status: bool = True
    type: Optional[str] = 'sale'
    category_id: Optional[int] = 1


    @field_validator('price', mode="before")
    def validate_price(cls, value):
        if value >= 0:
            return value
        else:
            raise ValueError("price must be more than 0")

    @model_validator(mode="before")
    def validation_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return SAnnouncement(**json.loads(value))
        return value

class SAnnouncementGet(SAnnouncement):
    id: int
    user_rel: Optional[SUser] = Field(None, description="Данные пользователя")
    file_rel: List[SFileGet] = Field(default_factory=list, description="Список файлов")

    model_config = ConfigDict(from_attributes=True)



class Filters(BaseModel):
    category_id: Optional[int | None] = Field(None, description='Категория')
    min_price: Optional[float | None] = Field(None,ge=1, le=100000000, description="Минимальная цена" )
    max_price: Optional[float | None] = Field(None,ge=1, description="Максимальная цена")
    geo: Optional[str | None] = Field(None, description='Город поиска')
    type: Optional[str| None] = Field(None, description='Тип объявления')

FiltersDep = Annotated[Filters, Depends()]

class Pagination(BaseModel):
    limit: int = Field(10, ge=0, le=100, description="Кол-во записей на странице")
    offset: int = Field(0, ge=0, description='Начало пагинации')


PaginationDep = Annotated[Pagination, Depends()]

