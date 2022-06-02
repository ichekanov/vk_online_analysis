from models import User
from sqlalchemy import select
from sqlalchemy.orm import Session


def find_user_by_id(db_session: Session, user_id: int) -> User:
    """
    Функция для поиска пользователя по id в базе данных

    Параметры
    ---------
    db_session: Session
        сессия SQLAlchemy подключения к базе данных
    user_id : int
        id пользователя в базе данных

    Возвращаемое значение
    ---------------------
    result : User
        Объект класса User

    Автор
    -----
    Иван Чеканов
    """
    query = select(User).where(User.id == user_id)
    result = db_session.execute(query).one()[0]
    return result
