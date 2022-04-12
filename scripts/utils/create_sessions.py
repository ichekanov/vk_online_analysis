from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert

from models import Activity, session


def create_sessions(intervals: list[dict], user_id: int):
    """
    Функция для создания большого количества записей о сессиях пользователя

    Параметры
    ---------
    intervals : list[dict]
        Список словарей вида
            `{"start": datetime.datetime, 
            "end": datetime.datetime, 
            "platform": int}`
        содержащих информацию о начале и конце сессии, а так же платформе,
        с которой она совершалась
    user_id : int
        Внутренний инедтификатор пользователя (из базы данных)

    Автор
    -----
    Иван Чеканов
    """
    for slot in intervals:
        try:
            query = insert(Activity).values(
                user_id=user_id,
                session_start=slot["start"],
                session_end=slot["end"],
                platform_id=slot["platform"]
            )
            session.execute(query)
        except IntegrityError:
            session.rollback()
            print("Session already exists.")
    session.commit()
