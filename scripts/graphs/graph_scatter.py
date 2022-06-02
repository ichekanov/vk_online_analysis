from datetime import datetime, timedelta

from pandas import date_range
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from utils.find_sessions_by_period import \
    find_sessions_by_period
from sqlalchemy.orm import Session


def graph_scatter(db_session: Session, start: datetime, end: datetime) -> Figure:
    '''
    Функция для выбранного интервала дат создаёт диаграмму рассеяния, показывающую
    зависимость длительности сессии от времени её начала.

    Параметры
    ---------
    db_session: Session
        сессия SQLAlchemy подключения к базе данных
    start : datetime.datetime
        начало временного промежутка
    end : datetime.datetime
        конец временного промежутка

    Возвращаемое значение
    ---------------------
    fig : matplotlib.figure.figure
        объект figure с одним графиком и необходимыми подписями к нему

    Автор
    -----
    Иван Чеканов
    '''
    session_length = []
    session_start = []
    start_timestamps = date_range(start, end, freq="1H", closed="left")
    for i, begin in enumerate(start_timestamps):
        sessions = find_sessions_by_period(
            db_session, begin, begin+timedelta(hours=1), False)
        for session in sessions:
            delta = (session.session_end -
                     session.session_start).seconds
            session_length.append(delta/60)
            session_start.append(session.session_start)
    fig, ax = plt.subplots(dpi=100, figsize=(12, 7))
    ax.scatter(session_start, session_length, s=0.5)
    ax.set_ylim([0, 60])
    ax.set_title("Длительность сессий в зависимости от времени в период {} -- {}".format(
        start.strftime("%d.%m.%Y %H:%M"),
        end.strftime("%d.%m.%Y %H:%M")
    ))
    ax.set_xlabel("Время начала сессии")
    ax.set_ylabel("Длительность сессии, минут")
    fig.set_facecolor("w")
    fig.tight_layout()
    return fig
