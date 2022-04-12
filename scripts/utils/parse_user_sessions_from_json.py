import json

from .create_sessions import create_sessions
from .find_user_by_name import find_user_by_name


def parse_user_sessions_from_json(path_to_file: str):
    """
    Функция для чтения «промежуточных» данных из json файлов и записи
    полученной информации в базу данных. Работает только для пользователей,
    уже находящихся в базе данных.

    Параметры
    ---------
    path_to_file : str
        Полный путь к файлу, содержащему обработанные данные

    Автор
    -----
    Иван Чеканов
    """
    with open(path_to_file, encoding="utf-8") as file:
        data = json.load(file)
    user = find_user_by_name(data.keys()[0])
    create_sessions(list(data.values()), user.id)
