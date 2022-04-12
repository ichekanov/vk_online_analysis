from models import User, session
from sqlalchemy import select


def find_user_by_name(name: str) -> User:
    """
    Функция для поиска пользователя по имени в базе данных

    Параметры
    ---------
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
    result = session.execute(query).one()
    return result
