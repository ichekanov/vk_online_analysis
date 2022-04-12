from models import User, session
from sqlalchemy import select


def find_user_by_id(user_id: int) -> User:
    """
    Функция для поиска пользователя по id в базе данных

    Параметры
    ---------
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
    result = session.execute(query).one()
    return result
