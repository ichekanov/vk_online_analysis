from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from utils.find_user_sessions_by_period import \
    find_user_sessions_by_period
from utils.find_user_by_id import find_user_by_id
from sqlalchemy.orm import Session
from utils.get_platforms import get_platforms


def graph_bars_accumulated_by_platforms(db_session: Session, user_ids: list[int], start: datetime, end: datetime) -> Figure:
    '''
    Функция для выбранных пользователей генерирует столбчатый график их
    суммарного времени в сети за указанный промежуток времени.

    Параметры
    ---------
    db_session: Session
        сессия SQLAlchemy подключения к базе данных
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
    platforms = {m.id: m.description for m in get_platforms(db_session)}
    guys = {}
    for user_id in user_ids:
        user = find_user_by_id(db_session, user_id)
        guys[user.id] = user.name
    active_users = {user_id: {platform_id: 0 for platform_id in platforms.keys()} for user_id in user_ids}
    for user_id in user_ids:
        sessions = find_user_sessions_by_period(db_session, user_id, start, end)
        for session in sessions:
            active_users[session.user_id][session.platform_id] += (session.session_end-session.session_start).total_seconds()
    fig, ax = plt.subplots(dpi=100, figsize=(12, 7))
    for i, platform in enumerate(platforms.values()):
        accum = [sum(list(m.values())[:i])/60 for m in active_users.values()]
        curr = [list(m.values())[i]/60 for m in active_users.values()]
        ax.bar(guys.values(), curr, bottom=accum, label=platform)
    ax.set_title("Суммарное время в ВК за период {} -- {} для выбранных пользователей".format(
        start.strftime("%d.%m.%Y %H:%M"),
        end.strftime("%d.%m.%Y %H:%M")
    ))
    ax.set_ylabel("Время, минут")
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    plt.grid(True)
    fig.set_facecolor("w")
    fig.tight_layout()
    return fig
