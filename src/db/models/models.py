import enum
from sqlalchemy import Enum as SQLEnum
from typing import Optional, Annotated

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship


from config import Base


pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

class AnnouncementType(enum.Enum):
    sale = "sale"
    purchase = "purchase"


class UserModel(Base):
    __tablename__ = 'users'

    yandex_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(60))
    phone: Mapped[Optional[str]] = mapped_column(String(11))
    announcements_rel: Mapped[list["AnnouncementsModel"]]  = relationship(back_populates="user_rel")

class CategoriesModel(Base):
    __tablename__ = 'categories'

    id: Mapped[pk]
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    announcements_rel: Mapped[list["AnnouncementsModel"]] = relationship(back_populates="category_rel")


class AnnouncementsModel(Base):
    __tablename__ = 'announcements'

    id: Mapped[pk]
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(1024))
    price: Mapped[Optional[float]] = mapped_column()
    geo: Mapped[Optional[str]] = mapped_column(default='Не указана')
    type: Mapped[AnnouncementType] = mapped_column(SQLEnum(AnnouncementType, name='announcement_type'))
    status: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'users.yandex_id',
                   ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    user_rel: Mapped["UserModel"] = relationship(back_populates="announcements_rel")
    category_id = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'), index=True, nullable=False)
    category_rel: Mapped['CategoriesModel'] = relationship(back_populates="announcements_rel")
    image_1: Mapped[Optional[str]]
    image_2: Mapped[Optional[str]]
    image_3: Mapped[Optional[str]]
    image_4: Mapped[Optional[str]]
    image_5: Mapped[Optional[str]]
    image_6: Mapped[Optional[str]]
    image_7: Mapped[Optional[str]]
    image_8: Mapped[Optional[str]]
    image_9: Mapped[Optional[str]]
    image_10: Mapped[Optional[str]]
