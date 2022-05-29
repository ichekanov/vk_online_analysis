from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlQuery

from utils.find_user_by_id import find_user_by_id

class TextReport2(QtWidgets.QTableWidget):
    def __init__(self, sessions, connection):
        super().__init__()

        Plats = QSqlQuery()
        Plats.exec(
            """
            SELECT id,slug FROM platform
            """
        )
        id_to_slug = {}
        while Plats.next():
            id_to_slug.update({Plats.value(0): Plats.value(1)})

        active_users = {}
        for session in sessions:
            if session[0].user_id not in active_users:
                # id - name count plats
                active_users.update({session[0].user_id: [find_user_by_id(session[0].user_id)[0].name,1,[session[0].platform_id]]})
            else:
                active_users[session[0].user_id][1] += 1
                if session[0].platform_id not in active_users[session[0].user_id][2]:
                    active_users[session[0].user_id][2].append(session[0].platform_id)

        self.setRowCount(len(active_users))
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Id Пользователя","Имя", "Число сессий", "Платформы"])

        i = 0
        for (key, val) in active_users.items():
            print(key, val)
            a1 = [QtWidgets.QTableWidgetItem(str(key)),QtWidgets.QTableWidgetItem(val[0]),
                  QtWidgets.QTableWidgetItem(str(val[1]))]
            s = ""
            for j in val[2]:
                s = s + id_to_slug[j] + " "
            a1.append(QtWidgets.QTableWidgetItem(s))

            self.setItem(i, 0, a1[0])
            self.setItem(i, 1, a1[1])
            self.setItem(i, 2, a1[2])
            self.setItem(i, 3, a1[3])
            i += 1