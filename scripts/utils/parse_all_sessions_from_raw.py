from datetime import datetime
from sys import path

from pandas import date_range
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .create_sessions import create_sessions
from .get_users import get_users
from .initialize_db import initialize_db


def parse_all_sessions_from_raw(path_to_folder: str, start_date: datetime, end_date: datetime):
    """
    Функция для чтения «сырых» данных из csv файлов, обработки и записи 
    полученной информации в базу данных

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
    
    path.append("../")
    engine = create_engine("sqlite:///../data/new.db")
    db_session = sessionmaker(engine)()
    
    initialize_db(db_session)

    daterange = date_range(start_date, end_date)
    filenames = [m.strftime("%d-%m-%Y") for m in daterange]
    users = get_users()

    for i in range(1, len(list(users))+1):
        times = []
        activity = []
        for name in filenames:
            # file = open(f"../scrapper/data/{name}.csv")
            file = open(f"{path_to_folder}/{name}.csv")
            lines = file.readlines()
            lines = [m.split(", ") for m in lines]
            file.close()
            times += [int(m[0]) for m in lines]
            activity += [int(m[i]) for m in lines]
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
        create_sessions(db_session, online, i)
