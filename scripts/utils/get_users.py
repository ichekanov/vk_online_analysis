from ..models import User, session


def get_users() -> list[User]:
    """
    Функция для списка всех пользователей из базы данных

    Возвращаемое значение
    ---------------------
    list[User]
        Ответ базы данных со списком объектов класса User

    Автор
    -----
    Иван Чеканов
    """
    result = session.query(User)
    return result
