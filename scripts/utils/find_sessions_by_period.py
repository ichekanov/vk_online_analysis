from datetime import datetime

from models import Activity
from sqlalchemy import and_, select
from sqlalchemy.orm import Session


def find_sessions_by_period(db_session: Session, start_date: datetime, end_date: datetime, cut: bool = False) -> list[Activity]:
    """
    Функция для поиска всех сессий от начальной до конечной даты в базе данных.

    Параметры
    ---------
    db_session: Session
        сессия SQLAlchemy подключения к базе данных
    start_date : datetime.datetime
        Время, с которого нужно начать поиск
    end_date : datetime.datetime
        Время, на котором нужно остановить поиск
    cut : bool
        Если False, то ищутся все сессии, частично входящие в промежуток. Иначе учитываются только полностью лежащие в выбранном промежутке

    Возвращаемое значение
    ---------------------
    result : list[Activity]
        Список объектов класса Activity

    Автор
    -----
    Иван Чеканов
    """
    if cut:
        query = select(Activity).where(and_(
            Activity.session_start > start_date, Activity.session_end < end_date))
    else:
        query = select(Activity).where(and_(
            Activity.session_end > start_date, Activity.session_start < end_date))
    result = [m[0] for m in db_session.execute(query)]
    return result
