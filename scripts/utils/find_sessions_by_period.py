from datetime import datetime, timedelta

from models import Activity, session
from sqlalchemy import and_, select


def find_sessions_by_period(start_date: datetime, end_date: datetime, cut_finish: bool = True) -> list[Activity]:
    """
    Функция для поиска всех сессий от начальной до конечной даты в базе данных.

    Параметры
    ---------
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
    if cut_finish:
        query = select(Activity).where(and_(
            Activity.session_start > start_date, Activity.session_end < end_date))
    else:
        query = select(Activity).where(and_(
            Activity.session_start > start_date, Activity.session_start < end_date))
    result = session.execute(query)
    return result
