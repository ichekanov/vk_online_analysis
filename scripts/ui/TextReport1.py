from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlQuery

from utils.find_user_sessions_by_period import find_user_sessions_by_period
from utils.find_user_by_id import find_user_by_id

class TextReport1(QtWidgets.QTableWidget):
    def __init__(self, users, t_start, t_end, connection):
        super().__init__()
        # id - name plats sessions
        sessions = []

        for user in users:
            for session in find_user_sessions_by_period(user,t_start,t_end):
                sessions.append(session)
        print(sessions)

        self.setRowCount(len(sessions))
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Id Пользователя","Имя", "Платформа", "Сессия"])

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
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(str(session[0].user_id)))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(find_user_by_id(session[0].user_id)[0].name))
            self.setItem(i, 2, QtWidgets.QTableWidgetItem(id_to_slug[session[0].platform_id]))
            self.setItem(i, 3, QtWidgets.QTableWidgetItem(str(session[0].session_start) + " - " + str(session[0].session_end)))
            i += 1

