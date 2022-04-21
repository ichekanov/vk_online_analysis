from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from utils.find_sessions_by_period import \
    find_sessions_by_period


def graph_histogram_sessions(start: datetime, end: datetime) -> Figure:
    '''
    Функция для выбранного интервала дат создаёт гистограмму
    распределения длительностей сессий.

    Параметры
    ---------
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
    sessions = find_sessions_by_period(start, end)
    for session in sessions:
        delta = (session[0].session_end -
                        session[0].session_start).seconds
        #! Без такого ограничения не получается адекватная гистограмма, т.к. кривой скрипт наполнения БД
        if delta < 3600:
            wasted_time.append(delta/60)
        elif delta > 36000:
            print(session)
    fig, ax = plt.subplots(dpi=100, figsize=(12, 7))
    ax.hist(wasted_time, bins=60, rwidth=0.8)
    ax.set_title("Распределение длительностей сессий в период {} -- {}".format(
        start.strftime("%d.%m.%Y %H:%M"),
        end.strftime("%d.%m.%Y %H:%M")
    ))
    ax.set_xlabel("Время, минут")
    ax.set_ylabel("Количество сессий")
    fig.set_facecolor("w")
    fig.tight_layout()
    return fig
