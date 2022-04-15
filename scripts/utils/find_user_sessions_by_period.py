from datetime import datetime, timedelta

from models import Activity, session
from sqlalchemy import and_, select


def find_user_sessions_by_period(user_id: int, start_date: datetime, end_date: datetime) -> list[Activity]:
    """
    Функция для поиска сессий определенного пользователя от начальной
    до конечной даты в базе данных.

    Параметры
    ---------
    user_id : int
        id пользователя в базе данных
    start_date : datetime.datetime
        Время, с которого нужно начать поиск
    end_date : datetime.datetime
        Время, на котором нужно остановить поиск

    Возвращаемое значение
    ---------------------
    result : list[Activity]
        Список объектов класса Activity

    Автор
    -----
    Иван Чеканов
    """
    query = select(Activity).where(and_(
        Activity.session_start > start_date,
        Activity.session_end < end_date,
        Activity.user_id == user_id
    ))
    result = session.execute(query)
    return result
