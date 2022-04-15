from datetime import datetime, timedelta

from pandas import date_range
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from utils.find_sessions_by_period_and_user_id import \
    find_sessions_by_period_and_user_id
from utils.find_user_by_id import find_user_by_id


def graph_boxplot_daily(user_ids: list[int], start: datetime, end: datetime) -> Figure:
    '''
    Функция для выбранных пользователей генерирует диаграмму Бокса-Уискера, 
    показывающую время, проведенное во ВКонтакте в дни из указанного промежутка.

    Параметры
    ---------
    user_ids : list[int]
        id пользователей, о которых требуется получить информацию
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
    guys = []
    wasted_time = [[] for _ in user_ids]
    for i, user in enumerate(user_ids):
        guys.append(find_user_by_id(user)[0].name)
        for day in date_range(start, end):
            sessions = find_sessions_by_period_and_user_id(
                user, day, day+timedelta(1))
            time_in_day = 0
            for session in sessions:
                time_in_day += (session[0].session_end -
                                session[0].session_start).seconds
            wasted_time[i].append(time_in_day/60)
    fig, ax = plt.subplots(dpi=100, figsize=(12, 7))
    ax.boxplot(wasted_time, labels=guys)
    ax.set_title("Время в ВК по дням за период {} -- {} для выбранных пользователей".format(
        start.strftime("%d.%m.%Y %H:%M"),
        end.strftime("%d.%m.%Y %H:%M")
    ))
    ax.set_ylabel("Время, минут")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True)
    fig.set_facecolor("w")
    fig.tight_layout()
    return fig
