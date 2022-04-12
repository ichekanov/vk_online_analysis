from ..models import User, session


def find_user_by_name(name: str) -> User:
    """
    Функция для поиска пользователя по имени в базе данных

    Автор
    -----
    Иван Чеканов
    """
    result = session.query(User.name == name)
    return result
