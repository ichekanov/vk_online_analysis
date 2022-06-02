from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from utils.find_sessions_by_period import \
    find_sessions_by_period
from sqlalchemy.orm import Session


def graph_histogram_sessions(db_session: Session, start: datetime, end: datetime) -> Figure:
    '''
    Функция для выбранного интервала дат создаёт гистограмму
    распределения длительностей сессий.

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
    Егор Волков
    '''
    wasted_time = []
    sessions = find_sessions_by_period(db_session, start, end)
    for session in sessions:
        delta = (session.session_end -
                        session.session_start).total_seconds()
        wasted_time.append(delta/60)
    fig, ax = plt.subplots(dpi=100, figsize=(12, 7))
    n = int(max(wasted_time))
    ax.hist(wasted_time, bins=n, rwidth=0.8)
    ax.set_title("Распределение числа сессий по длительности в период {} -- {}".format(
        start.strftime("%d.%m.%Y %H:%M"),
        end.strftime("%d.%m.%Y %H:%M")
    ))
    ax.set_xlim([0, 60])
    ax.set_xlabel("Время, минут")
    ax.set_ylabel("Количество сессий")
    fig.set_facecolor("w")
    fig.tight_layout()
    return fig
