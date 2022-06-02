from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert

from models import Platform
from sqlalchemy.orm import Session



def create_platform(db_session: Session, slug: str, description: str):
    """
    Функция для добавления информации о платформе в базу данных

    Параметры
    ---------
    db_session: Session
        сессия SQLAlchemy подключения к базе данных
    slug : str
        Короткое название (имя переменной класса Platforms)
    description : str
        Полное название (значение переменной класса Platforms)

    Автор
    -----
    Иван Чеканов
    """
    try:
        query = insert(Platform).values(slug=slug, description=description)
        db_session.execute(query)
    except IntegrityError:
        db_session.rollback()
        print("Platform already exists.")
    else:
        db_session.commit()
