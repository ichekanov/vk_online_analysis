from utils.create_platform import create_platform
from utils.create_user import create_user

from ..constants.platforms import Platforms
from ..constants.users import USERS


def initialize_db():
    """
    Функция для первоначального заполнения созданной базы данных

    Автор
    -----
    Иван Чеканов
    """
    for name, vk_id in zip(USERS.keys(), USERS.values()):
        create_user(name, vk_id)

    for platform in Platforms:
        create_platform(platform.name, platform.value)
