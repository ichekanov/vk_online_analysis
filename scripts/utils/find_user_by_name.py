from models import User
from sqlalchemy import select
from sqlalchemy.orm import Session


def find_user_by_name(db_session: Session, name: str) -> User:
    """
    Функция для поиска пользователя по имени в базе данных

    Параметры
    ---------
    db_session: Session
        сессия SQLAlchemy подключения к базе данных
    name : str
        id пользователя в базе данных

    Возвращаемое значение
    ---------------------
    result : User
        Объект класса User

    Автор
    -----
    Иван Чеканов
    """
    query = select(User).where(User.name == name)
    result = db_session.execute(query).one()[0]
    return result
