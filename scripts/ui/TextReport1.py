from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlQuery

from utils.find_user_sessions_by_period import find_user_sessions_by_period
from utils.find_user_by_id import find_user_by_id
from sqlalchemy.orm import Session
from datetime import datetime
from PyQt5.QtSql import QSqlDatabase


class TextReport1(QtWidgets.QTableWidget):
    '''
    Класс, описывающий текстовый отчёт "Список сессий за выбранный период"

    Автор
    -----
    Илья Абрамов, Иван Чеканов
    '''
    def __init__(self, db_session: Session, connection: QSqlDatabase, users: list[int], t_start: datetime, t_end: datetime):
        '''
        Метод инициализации класса, описывающего текстовый отчёт "Список сессий за выбранный период"

        Автор
        -----
        Илья Абрамов
        '''
        super().__init__()
        # id - name plats sessions
        sessions = []

        for user in users:
            for session in find_user_sessions_by_period(db_session, user, t_start, t_end):
                sessions.append(session)

        self.setRowCount(len(sessions))
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(
            ["Id Пользователя", "Имя", "Платформа", "Сессия"])

        Plats = QSqlQuery()
        Plats.exec(
            """
            SELECT id,slug FROM platform
            """
        )
        id_to_slug = {}
        while Plats.next():
            id_to_slug.update({Plats.value(0): Plats.value(1)})

        i = 0
        for session in sessions:
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(
                str(session.user_id)))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(
                find_user_by_id(db_session, session.user_id).name))
            self.setItem(i, 2, QtWidgets.QTableWidgetItem(
                id_to_slug[session.platform_id]))
            self.setItem(i, 3, QtWidgets.QTableWidgetItem(
                str(session.session_start) + " - " + str(session.session_end)))
            i += 1

    def saveReport(self, db_session: Session):
        '''
        Метод сохранения созданного текстового отчёта

        Автор
        -----
        Иван Чеканов
        '''
        filepath = QtWidgets.QFileDialog().getSaveFileName(
            filter="Текстовый документ (*.txt);;Таблица CSV (*.csv)")[0]
        if not filepath:
            return False
        n = self.rowCount()
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write("Id Пользователя, Имя, Платформа, Сессия\n")
            for i in range(n):
                user_id = self.item(i, 0).text()
                user_name = self.item(i, 1).text()
                session_platform = self.item(i, 2).text()
                session_time = self.item(i, 3).text()
                file.write(", ".join([user_id, user_name, session_platform, session_time]))
                file.write("\n")
        return True
