from PyQt5.QtWidgets import QFileDialog
from utils.get_users import get_users
from sqlalchemy.orm import Session


def save_users(db_session: Session):
    filepath = QFileDialog().getSaveFileName(
        filter="Текстовый документ (*.txt);;Таблица CSV (*.csv)")[0]
    if not filepath:
        return
    users = get_users(db_session)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write("DB id, name, VK id\n")
        for user in users:
            file.write(user.__str__())
            file.write("\n")
