from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert

from models import User, session


def create_user(name: str, vk_id: int):
    """
    Функция для добавления информации о пользователе в базу данных

    Параметры
    ---------
    name : str
        Имя пользователя
    vk_id : int
        Идентификатор пользователя в сети ВКонтакте

    Автор
    -----
    Иван Чеканов
    """
    try:
        query = insert(User).values(name=name, vk_id=vk_id)
        session.execute(query)
    except IntegrityError:
        session.rollback()
        print("User already exists.")
    else:
        session.commit()
