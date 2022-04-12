from enum import Enum, unique

@unique
class Platforms(Enum):
    """
    Класс, описывающий платформы, с которых пользователь
    мог заходить во ВКонтакте.

    Автор
    -----
    Иван Чеканов
    """
    WEB_MOBILE = "Мобильная версия сайта"
    IPHONE = "Приложение для iPhone"
    IPAD = "Приложение для iPad"
    ANDROID = "Приложение для Android"
    WINDOWS_PHONE = "Приложение для Windows Phone"
    WINDOWS_APP = "Приложение для Windows 10"
    WEB = "Полная версия сайта"
    UNDEFINED = "Невозможно определить"
