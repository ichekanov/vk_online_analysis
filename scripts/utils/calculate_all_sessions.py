import json
from datetime import datetime

from pandas import date_range

from .get_users import get_users


def calculate_all_sessions(path_to_folder: str, start_date: datetime, end_date: datetime):
    """
    Функция для чтения «сырых» данных из csv файлов, обработки и записи 
    полученной информации в промежуточный формат json, удобный для чтения 
    человеком и не требующий специальной обработки

    Параметры
    ---------
    path_to_folder : str
        Путь к папке с файлами без последнего знака "/"
    start_date : datetime.datetime
        Дата, в которую был записан первый файл в папке
    end_date : datetime.datetime
        Дата, в которую был записан последний файл в папке

    Автор
    -----
    Иван Чеканов
    """
    def round5(number):
        return round(number * 2, -1) // 2

    daterange = date_range(start_date, end_date)
    filenames = [m.strftime("%d-%m-%Y") for m in daterange]
    users = get_users()

    for user in users:
        times = []
        activity = []
        for name in filenames:
            file = open(f"{path_to_folder}/{name}.csv")
            lines = file.readlines()
            lines = [m.split(", ") for m in lines]
            file.close()
            times += [int(m[0]) for m in lines]
            activity += [int(m[user.id]) for m in lines]
        online = []
        platform = -1
        start = 0
        end = 0
        for timestamp, state in zip(times, activity):
            if start and end and state != platform:
                online.append({
                    "start": datetime.fromtimestamp(start),
                    "end": datetime.fromtimestamp(end),
                    "platform": platform
                })
                start = 0
                end = 0
                platform = -1
            if state != 0 and start:
                end = round5(timestamp)
            if state != 0 and not start:
                start = round5(timestamp)
                platform = state
        json.dump(
            {user.name: online},
            open(f"{user.name}.csv", "w", encoding="utf-8")
        )
