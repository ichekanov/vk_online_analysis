from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from utils.find_sessions_by_period_and_user_id import \
    find_sessions_by_period_and_user_id
from utils.find_user_by_id import find_user_by_id


def graph_bars_accumulated(user_ids: list[int], start: datetime, end: datetime) -> Figure:
    '''
    Функция для выбранных пользователей генерирует столбчатый график их
    суммарного времени в сети за указанный промежуток времени.

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
    Яна Евдокимова
    '''
    guys = []
    wasted_time = []
    err = []
    for user in user_ids:
        guys.append(find_user_by_id(user)[0].name)
        sessions = find_sessions_by_period_and_user_id(user, start, end)
        wasted_time.append(0)
        i = 0
        for session in sessions:
            i += 1
            delta = session[0].session_end - session[0].session_start
            wasted_time[-1] += delta.seconds/60
        err.append(i)
    fig, ax = plt.subplots(dpi=100, figsize=(12, 7))
    ax.bar(guys, wasted_time, yerr=err)
    ax.set_title("Суммарное время в ВК за период {} -- {} для выбранных пользователей".format(
        start.strftime("%d.%m.%Y %H:%M"),
        end.strftime("%d.%m.%Y %H:%M")
    ))
    ax.set_ylabel("Время, минут")
    # plt.text(18.3,165,"Чёрным цветом обозначена погрешность")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True)
    fig.set_facecolor("w")
    fig.tight_layout()
    return fig
