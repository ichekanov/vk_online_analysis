"""
Описание моделей базы данных

Автор
-----
Иван Чеканов
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint


Base = declarative_base()

class Activity(Base):
    """
    Модель таблицы активности
    """
    __tablename__ = "activity"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    session_start = Column(DateTime, nullable=False)
    session_end = Column(DateTime, nullable=False)
    platform_id = Column(Integer, ForeignKey("platform.id"), nullable=False)
    UniqueConstraint(user_id, session_start)

    def __repr__(self):
        info = "Activity(user_id={}, session_start={}, session_end={}, platform_id={})"
        return info.format(
            self.user_id,
            self.session_start,
            self.session_end,
            self.platform_id
        )


class User(Base):
    """
    Модель таблицы пользователей
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    vk_id = Column(Integer, nullable=False)
    university_group = Column(Integer, nullable=True)
    UniqueConstraint(vk_id)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, vk_id={self.vk_id!r})"
    
    def __str__(self) -> str:
        return f"{self.id!r}, {self.name!r}, {self.vk_id!r}"


class Platform(Base):
    """
    Модель таблицы платформ
    """
    __tablename__ = "platform"
    id = Column(Integer, primary_key=True)
    slug = Column(String(32), nullable=False)
    description = Column(String(128), nullable=False)
    UniqueConstraint(slug, description)

    def __repr__(self):
        return (f"Platform(id={self.id!r}, short_name={self.slug!r}, "
                f"full_name={self.description!r})")
    
    def __str__(self) -> str:
        return f"{self.id!r}, {self.slug!r}, {self.description!r}"

