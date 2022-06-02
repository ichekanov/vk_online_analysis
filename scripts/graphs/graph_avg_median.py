from datetime import datetime, timedelta
from statistics import median as count_median

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from pandas import date_range
from sqlalchemy.orm import Session
from utils.find_sessions_by_period import find_sessions_by_period


def graph_avg_median(db_session: Session, start: datetime, end: datetime) -> Figure:
    '''
    Функция показывает разницу между средним и медианным временем 
    по часам выбранного интервала.

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
    avg = []
    median = []
    timestamps = date_range(start, end, freq="1H")
    for timestamp in timestamps:
        sessions = find_sessions_by_period(db_session, timestamp, timestamp+timedelta(hours=1), cut=True)
        deltas = []
        for session in sessions:
            delta = (session.session_end - session.session_start).total_seconds()
            deltas.append(delta)
        avg.append(sum(deltas)/len(deltas)/60)
        median.append(count_median(deltas)/60)
    fig, ax = plt.subplots(dpi=100, figsize=(12, 7))
    plt.xticks(rotation=45, ha="right")
    plt.grid(True)
    ax.bar(timestamps, avg, label="Средняя продолжительность", width=0.01)
    ax.plot(timestamps, median, label="Медианная продолжительность", color='orange')
    ax.set_ylabel("Время, минут")
    ax.set_ylim([0, max(avg)])
    ax.set_title("Сравнение медианной и среднеарифметической длительности сессии в период {} -- {}".format(
        start.strftime("%d.%m.%Y %H:%M"),
        end.strftime("%d.%m.%Y %H:%M")
    ))
    ax.legend(loc='upper right')
    fig.set_facecolor("w")
    fig.tight_layout()
    return fig
