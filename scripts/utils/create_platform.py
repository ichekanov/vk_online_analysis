from sqlite3 import IntegrityError
from sqlalchemy import insert

from ..models import Platform, session


def create_platform(slug: str, description: str):
    """
    Функция для добавления информации о платформе в базу данных

    Параметры
    ---------
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
        session.execute(query)
    except IntegrityError:
        session.rollback()
        print("Platform already exists.")
    else:
        session.commit()
