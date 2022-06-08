from PyQt5.QtWidgets import QFileDialog
from utils.get_platforms import get_platforms
from sqlalchemy.orm import Session


def save_platforms(db_session: Session):
    filepath = QFileDialog().getSaveFileName(
        filter="Текстовый документ (*.txt);;Таблица CSV (*.csv)")[0]
    if not filepath:
        return
    platforms = get_platforms(db_session)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write("DB id, slug, description\n")
        for platform in platforms:
            file.write(platform.__str__())
            file.write("\n")
