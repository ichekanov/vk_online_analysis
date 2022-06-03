from datetime import datetime
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtSql import QSqlQuery

from sqlalchemy.orm import Session

from utils.find_user_by_id import find_user_by_id
from utils.find_user_sessions_by_period import find_user_sessions_by_period


class TextReport3(QTableWidget):
    '''
    Класс, описывающий текстовый отчёт "Сводная таблица"

    Автор
    -----
    Илья Абрамов, Иван Чеканов
    '''
    def __init__(self, db_session: Session, users: list[int], start: datetime, end: datetime):
        '''
        Метод инициализации класса описывающего текстовый отчёт "Сводная таблица"

        Автор
        -----
        Илья Абрамов, Иван Чеканов
        '''
        super().__init__()

        Plats = QSqlQuery()
        Plats.exec(
            """
            SELECT id,description FROM platform
            """
        )
        self.platforms = {}
        while Plats.next():
            self.platforms.update({Plats.value(0): Plats.value(1)})

        self.active_users = {user_id: {platform_id: 0 for platform_id in self.platforms.keys()} for user_id in users}
        for user_id in users:
            sessions = find_user_sessions_by_period(db_session, user_id, start, end)
            for session in sessions:
                self.active_users[session.user_id][session.platform_id] += 1
        self.setRowCount(len(self.active_users))
        self.setColumnCount(len(self.platforms)+2)
        self.setHorizontalHeaderLabels(['Имя пользователя', 'Всего сессий']+[*self.platforms.values()])

        for i, (user_id, counter) in enumerate(self.active_users.items()):
            # print(counter)
            user_name = find_user_by_id(db_session, user_id).name
            self.setItem(i, 0, QTableWidgetItem(user_name))
            self.setItem(i, 1, QTableWidgetItem(str(sum(counter.values()))))
            for j, number in enumerate(counter.values()):
                self.setItem(i, j+2, QTableWidgetItem(str(number)))
        
        self.resizeColumnsToContents()


    def saveReport(self, db_session: Session):
        '''
        Метод сохранения созданного текстового отчёта

        Автор
        -----
        Иван Чеканов
        '''
        filepath = QFileDialog().getSaveFileName(
            filter="Текстовый документ (*.txt);;Таблица CSV (*.csv)")[0]
        if not filepath:
            return False
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(f"Имя пользователя, Всего сессий,{', '.join(self.platforms.values())}\n")
            for user_id, sessions in self.active_users.items():
                user_name = find_user_by_id(db_session, user_id).name
                counts = [str(m) for m in sessions.values()]
                total = str(sum(sessions.values()))
                file.write(", ".join([user_name, total, *counts]))
                file.write("\n")
        return True
