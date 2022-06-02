from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert

from models import User
from sqlalchemy.orm import Session


def create_user(db_session: Session, name: str, vk_id: int):
    """
    Функция для добавления информации о пользователе в базу данных

    Параметры
    ---------
    db_session: Session
        сессия SQLAlchemy подключения к базе данных
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
        db_session.execute(query)
    except IntegrityError:
        db_session.rollback()
        print("User already exists.")
    else:
        db_session.commit()
