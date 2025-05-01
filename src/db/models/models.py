import enum
import uuid
from datetime import datetime

import sqlalchemy
from sqlalchemy import Enum as SQLEnum, Boolean, text
from typing import Optional, Annotated

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship


from config import Base


pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE( 'utc', now())"))]

class AnnouncementType(enum.Enum):
    sale = "sale"
    purchase = "purchase"

class ReportsStatus(enum.Enum):
    unseen = 'unseen'
    denied = 'denied'
    allowed = 'allowed'

class ReportType(enum.Enum):
    spam = 'spam'
    ad = 'ad'
    other = 'other'


class UserModel(Base):
    __tablename__ = 'users'

    yandex_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(60))
    phone: Mapped[Optional[str]] = mapped_column(String(11))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id', ondelete='CASCADE'), default=1)
    announcements_rel: Mapped[list["AnnouncementsModel"]]  = relationship(back_populates="user_rel")
    roles_rel: Mapped["RoleModel"] = relationship(back_populates="user_rel")
    tokens_rel: Mapped[list["TokenModel"]] = relationship(back_populates="user_rel")
    reports_rel: Mapped[list["ReportModel"]] = relationship(back_populates="user_rel")


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
    created_at: Mapped[created_at]
    user_rel: Mapped["UserModel"] = relationship(back_populates="announcements_rel")
    category_id = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'), index=True, nullable=False)
    category_rel: Mapped['CategoriesModel'] = relationship(back_populates="announcements_rel")
    file_rel: Mapped[list["FileModel"]] = relationship(back_populates="announcements_rel")
    reports_rel: Mapped[list["ReportModel"]] = relationship(back_populates="announcement_rel")


class FileModel(Base):
    __tablename__ = 'files'

    id: Mapped[pk]
    announcement_id: Mapped[int] = mapped_column(ForeignKey('announcements.id', ondelete='CASCADE'))
    type: Mapped[str] = mapped_column(String(30))
    url: Mapped[str]
    announcements_rel: Mapped["AnnouncementsModel"] = relationship(back_populates="file_rel")



class RoleModel(Base):
    __tablename__ = 'roles'

    id: Mapped[pk]
    role: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    user_rel: Mapped[list["UserModel"]] = relationship(back_populates="roles_rel")


class TokenModel(Base):
    __tablename__ = 'tokens'

    id: Mapped[pk]
    token_id: Mapped[str] = mapped_column(unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.yandex_id', ondelete='CASCADE'))
    user_rel: Mapped['UserModel'] = relationship(back_populates="tokens_rel")
    is_banned: Mapped[bool] = mapped_column(default=False)
    issued_at: Mapped[created_at]


class ReportModel(Base):
    __tablename__ = 'reports'

    id: Mapped[pk]
    announcement_id: Mapped[int] = mapped_column(ForeignKey('announcements.id', ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.yandex_id', ondelete='CASCADE'))
    reason: Mapped[Optional[str]] = mapped_column(String(256))
    created_at: Mapped[created_at]
    status: Mapped[ReportsStatus] = mapped_column(SQLEnum(ReportsStatus, name='report_status'), default='unseen')
    type: Mapped[ReportType] = mapped_column(SQLEnum(ReportType, name='report_type'), default='unseen')
    user_rel: Mapped['UserModel'] = relationship(back_populates="reports_rel")
    announcement_rel: Mapped['AnnouncementsModel'] = relationship(back_populates='reports_rel')