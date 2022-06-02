from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlQuery

from utils.find_user_by_id import find_user_by_id
from utils.find_sessions_by_period import find_sessions_by_period
from sqlalchemy.orm import Session
from datetime import datetime


class TextReport2(QtWidgets.QTableWidget):
    '''
    Класс, описывающий текстовый отчёт "Список активных пользователей за выбранный период"

    Автор
    -----
    Илья Абрамов, Иван Чеканов
    '''
    def __init__(self, db_session: Session, start: datetime, end: datetime):
        '''
        Метод инициализации класса, описывающего текстовый отчёт "Список активных пользователей за выбранный период"

        Автор
        -----
        Илья Абрамов
        '''
        super().__init__()
        sessions = find_sessions_by_period(db_session, start, end)

        Plats = QSqlQuery()
        Plats.exec(
            """
            SELECT id,description FROM platform
            """
        )
        id_to_description = {}
        while Plats.next():
            id_to_description.update({Plats.value(0): Plats.value(1)})

        active_users = {}
        for session in sessions:
            if session.user_id not in active_users:
                # id - name count plats
                active_users.update({session.user_id: [find_user_by_id(
                    db_session, session.user_id).name, 1, [session.platform_id]]})
            else:
                active_users[session.user_id][1] += 1
                if session.platform_id not in active_users[session.user_id][2]:
                    active_users[session.user_id][2].append(
                        session.platform_id)

        self.setRowCount(len(active_users))
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(
            ["Id Пользователя", "Имя", "Число сессий", "Платформы"])

        i = 0
        for (key, val) in active_users.items():
            # print(key, val)
            a1 = [QtWidgets.QTableWidgetItem(str(key)), QtWidgets.QTableWidgetItem(val[0]),
                  QtWidgets.QTableWidgetItem(str(val[1]))]
            s = ""
            for j in val[2]:
                s = s + id_to_description[j] + "; "
            a1.append(QtWidgets.QTableWidgetItem(s))

            self.setItem(i, 0, a1[0])
            self.setItem(i, 1, a1[1])
            self.setItem(i, 2, a1[2])
            self.setItem(i, 3, a1[3])
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
            file.write("Id Пользователя, Имя, Число сессий, Платформы\n")
            for i in range(n):
                user_id = self.item(i, 0).text()
                user_name = self.item(i, 1).text()
                sessions_count = self.item(i, 2).text()
                sessions_platforms = self.item(i, 3).text()
                file.write(", ".join([user_id, user_name, sessions_count, sessions_platforms]))
                file.write("\n")
        return True
