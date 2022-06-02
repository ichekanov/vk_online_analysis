from models import Platform
from sqlalchemy.orm import Session


def get_platforms(db_session: Session) -> list[Platform]:
    """
    Функция для списка всех пользователей из базы данных

    Возвращаемое значение
    ---------------------
    db_session: Session
        сессия SQLAlchemy подключения к базе данных
    list[Platform]
        Ответ базы данных со списком объектов класса Platform

    Автор
    -----
    Иван Чеканов
    """
    result = db_session.query(Platform)
    return result
