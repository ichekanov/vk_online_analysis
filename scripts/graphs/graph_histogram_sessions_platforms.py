from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from utils.find_sessions_by_period import \
    find_sessions_by_period
from sqlalchemy.orm import Session
from utils.get_platforms import get_platforms


def graph_histogram_sessions_platforms(db_session: Session, start: datetime, end: datetime) -> Figure:
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
    platforms = {m.id: m.description for m in get_platforms(db_session)}
    wasted_time = {m: [] for m in platforms.keys()}
    sessions = find_sessions_by_period(db_session, start, end)
    for session in sessions:
        delta = (session.session_end -
                        session.session_start).total_seconds()
        wasted_time[session.platform_id].append(delta/60)
    # sessions_by_platforms = [[15,1,2], [2,3,4], [17,13,25], [7,3,9]]
    sessions_by_platforms = [m for m in wasted_time.values()]
    n = int(max(max(m) for m in sessions_by_platforms if m))
    # print(sessions_by_platforms)
    fig, ax = plt.subplots(dpi=100, figsize=(12, 7))
    ax.hist(sessions_by_platforms, bins=n, rwidth=0.8, histtype='bar', stacked=True, label=list(platforms.values()))
    ax.set_title("Распределение числа сессий по длительности в период {} -- {}".format(
        start.strftime("%d.%m.%Y %H:%M"),
        end.strftime("%d.%m.%Y %H:%M")
    ))
    ax.set_xlim([0, 60])
    ax.set_xlabel("Время, минут")
    ax.set_ylabel("Количество сессий")
    ax.legend()
    fig.set_facecolor("w")
    fig.tight_layout()
    return fig
