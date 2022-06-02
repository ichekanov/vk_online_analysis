from datetime import datetime

from scripts.models import Activity
from sqlalchemy import and_, select
from sqlalchemy.orm import Session


def find_user_sessions_by_period(db_session: Session, user_id: int, start_date: datetime, end_date: datetime, cut: bool = False) -> list[Activity]:
    """
    Функция для поиска сессий определенного пользователя от начальной
    до конечной даты в базе данных.

    Параметры
    ---------
    db_session: Session
        сессия SQLAlchemy подключения к базе данных
    user_id : int
        id пользователя в базе данных
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
            Activity.session_start > start_date,
            Activity.session_end < end_date,
            Activity.user_id == user_id
        ))
    else:
        query = select(Activity).where(and_(
            Activity.session_end > start_date,
            Activity.session_start < end_date,
            Activity.user_id == user_id
        ))
    # result = db_session.execute(query)
    result = [m[0] for m in db_session.execute(query)]
    return result
