from datetime import datetime, timedelta

from models import Activity, session
from sqlalchemy import and_, select


def find_sessions_by_period(start_date: datetime, end_date: datetime) -> list[Activity]:
    """
    Функция для поиска всех сессий от начальной до конечной даты в базе данных.
    Для улучшения графиков start_date сдвигается на час назад, а end_date --
    на час вперёд.

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
    start_date = start_date - timedelta(hours=1)
    end_date = end_date + timedelta(hours=1)
    query = select(Activity).where(and_(
        Activity.session_start > start_date, Activity.session_end < end_date))
    result = session.execute(query)
    return result
