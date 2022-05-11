"""
Database initialization and connection establishment tool

Автор
-----
Иван Чеканов
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import UniqueConstraint


# DB_PATH = "/Users/ichek/Yandex.Disk.localized/code/project_sem_python/csv_processing/project.db"
DB_PATH = "data/project.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Activity(Base):
    """
    Activity model for database
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
    User model for database
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    vk_id = Column(Integer, nullable=False)
    university_group = Column(Integer, nullable=True)
    UniqueConstraint(vk_id)

    # def __init__(self, name: str, vk_id: int, university_group: int = None) -> None:
    #     self.name = name
    #     self.vk_id = vk_id
    #     if university_group:
    #         self.university_group = university_group

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, vk_id={self.vk_id!r})"


class Platform(Base):
    """
    Platform object for database
    """
    __tablename__ = 'platform'
    id = Column(Integer, primary_key=True)
    slug = Column(String(32), nullable=False)
    description = Column(String(128), nullable=False)
    UniqueConstraint(slug, description)

    def __repr__(self):
        return (f"Platform(id={self.id!r}, short_name={self.short_name!r}, "
                f"full_name={self.full_name!r})")


Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()
