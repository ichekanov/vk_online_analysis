from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from utils.find_sessions_by_period import find_sessions_by_period


def graph_line_online_counter(start: datetime, end: datetime) -> Figure:
    '''
    Функция генерирует линейный график количества пользователей в сети
    в течение указанного за указанный период.

    Параметры
    ---------
    user : int
        id пользователя, о котором требуется получить информацию
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
    start = start - timedelta(hours=1)
    end = end + timedelta(hours=1)
    data = find_sessions_by_period(start, end)
    time_tick = list(pd.date_range(start, end, freq='5S'))
    counter = {t: 0 for t in time_tick}
    for slot in data:
        tstamps = pd.date_range(max(slot[0].session_start, start), min(
            slot[0].session_end, end), freq='5S')
        for i in tstamps:
            counter[i] += 1
    counter = list(counter.values())
    fig, plt1 = plt.subplots()
    fig.set_dpi(100)
    fig.set_facecolor('w')
    fig.set_size_inches((17, 7))
    plt1.set_title('Активность пользователей в период {} — {}'.format(
        start.strftime("%d.%m.%Y %H:%M"), end.strftime("%d.%m.%Y %H:%M")))
    plt1.plot(time_tick, counter)
    plt1.set_xlim((start, end))
    time_tick = pd.date_range(start, end, freq='1H')
    time_tick_labels = [i.strftime('%H:%M') for i in time_tick]
    plt1.set_xticks(time_tick)
    plt1.set_xticklabels(time_tick_labels)
    plt1.set_xlabel('Время')
    plt1.set_ylabel('Количество пользователей в сети')
    fig.tight_layout()
    return fig
