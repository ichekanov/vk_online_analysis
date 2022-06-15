import colorsys
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from pandas.core.common import flatten
from utils.find_user_by_id import find_user_by_id
from utils.find_user_sessions_by_period import find_user_sessions_by_period
from sqlalchemy.orm import Session


def graph_daily_activity_multiple(db_session: Session, user_ids: list[int], start: datetime, end: datetime) -> Figure:
    '''
    Функция генерирует график активности пользователя с цветовой маркировкой
    длительности непрерывной сессии за указанный период.

    Параметры
    ---------
    db_session: Session
        сессия SQLAlchemy подключения к базе данных
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
    if len(user_ids) == 1:
        fig, plots = plt.subplots(nrows=1)
        plots = [plots]
    else:
        fig, [*plots] = plt.subplots(nrows=len(user_ids))
    for ax, user_id in zip(plots, user_ids):
        data = find_user_sessions_by_period(db_session, user_id, start, end)
        user_name = find_user_by_id(db_session, user_id).name
        # список списков, состоящих из timestamp с шагом 5 секунд и соответствющих
        # периодам активности пользователя
        period = [pd.date_range(session.session_start,
                                session.session_end, freq='5S') for session in data]
        # вспомогательный список, в котором хранятся цвета для заливки точек
        color = []
        # коэффициент скорости смены зеленого на красный
        KR = 0.12
        for slot in period:
            h = 120/360
            l = 1
            for _ in range(len(slot)):
                if h-0.015*KR > 0:
                    h -= 0.01*KR
                    l -= 0.002*KR
                elif l-0.01*KR > 0.5:
                    l -= 0.01*KR
                color += [colorsys.hsv_to_rgb(h, 1, l)]
        # преобразовываем двумерный массив в одномерный
        period = list(flatten(period))
        # список точек, которые будут окрашены в цвета
        activity = [1]*len(period)
        # временная шкала, вспомогательный список
        time_tick = pd.date_range(start, end, freq="1H")
        # фактически отображаемые на графике подписи оси Х
        time_tick_labels = [i.strftime("%H:%M") for i in time_tick]
        ax.set_title('Активность пользователя {} в период {} — {}'.format(
        user_name,
        start.strftime("%d.%m.%Y %H:%M"),
        end.strftime("%d.%m.%Y %H:%M")
        ))
        ax.scatter(period, activity, marker='o', c=color)
        ax.set_xlim((start, end))
        ax.set_xticks(time_tick)
        ax.set_xticklabels(time_tick_labels)
        ax.set_yticks([])
        ax.set_ylim((0.75, 1.25))
        ax.set_xlabel("Время")
    fig.set_facecolor('w')
    fig.tight_layout()
    return fig
