from models import User
from sqlalchemy.orm import Session



def get_users(db_session: Session) -> list[User]:
    """
    Функция для списка всех пользователей из базы данных

    Возвращаемое значение
    ---------------------
    db_session: Session
        сессия SQLAlchemy подключения к базе данных
    list[User]
        Ответ базы данных со списком объектов класса User

    Автор
    -----
    Иван Чеканов
    """
    result = db_session.query(User)
    return result
