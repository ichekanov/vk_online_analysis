from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from utils.find_sessions_by_period import find_sessions_by_period
from utils.get_platforms import get_platforms
from sqlalchemy.orm import Session


def graph_avg_time_by_platform(db_session: Session, start: datetime, end: datetime) -> Figure:
    '''
    Функция генерирует столбчатый график показывающий 
    различия в средней длительности сессий.

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
    width = 0.35
    data = {m.id: [m.description, 0, 0] for m in get_platforms(db_session)}
    sessions = find_sessions_by_period(db_session, start, end)
    for session in sessions:
        if session.platform_id not in data.keys():
            continue
        avg = data[session.platform_id][1] # среднее арифметическое длительности сессий
        n = data[session.platform_id][2] # число сессий
        delta = (session.session_end - session.session_start).total_seconds()
        data[session.platform_id][1] = (avg * n + delta) / (n + 1)
        data[session.platform_id][2] = n + 1
    platforms = [m[0] for m in data.values()]
    lengths = [m[1] for m in data.values()]
    numbers = [m[2] for m in data.values()]
    k = max(lengths)/max(numbers)
    adjusted_numbers = [m[2]*k*3 for m in data.values()]
    fig, ax1 = plt.subplots(dpi=100, figsize=(12, 7))
    plt.xticks(rotation=45, ha="right")
    plt.grid(True)
    bar = ax1.bar(platforms, lengths, width, label="Средняя продолжительность", color='orange')
    ax1.set_ylabel("Время, секунд")
    ax1.tick_params('y', colors='orange')
    ax1.yaxis.label.set_color('orange')
    ax2 = ax1.twinx()
    dot = ax2.scatter(platforms, numbers, label="Число сессий", s=adjusted_numbers, alpha=0.5)
    ax2.set_ylabel("Число сессий")
    ax2.tick_params('y', colors='C0')
    ax2.yaxis.label.set_color('C0')
    ax1.set_title("Зависимость средней длительности сессии в ВК от платформы в период {} -- {}".format(
        start.strftime("%d.%m.%Y %H:%M"),
        end.strftime("%d.%m.%Y %H:%M")
    ))
    ax1.legend(handles=[bar, dot], loc='upper right')
    fig.set_facecolor("w")
    fig.tight_layout()
    return fig
