# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
from datetime import datetime

sys.path.append('../')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel  # Работа с бд

from ui.dialog1 import Ui_Dialog as Ui_Dialog1
from ui.dialog2 import Ui_Dialog as Ui_Dialog2
from ui.TextReport1 import TextReport1
from ui.TextReport2 import TextReport2
from ui.TextReport3 import TextReport3
from ui.Graphs import GraphWidget

from graphs.graph_scatter import graph_scatter
from graphs.graph_histogram_sessions import graph_histogram_sessions
from graphs.graph_histogram_sessions_platforms import graph_histogram_sessions_platforms
from graphs.graph_bars_accumulated import graph_bars_accumulated
from graphs.graph_bars_accumulated_by_platforms import graph_bars_accumulated_by_platforms
from graphs.graph_boxplot_daily import graph_boxplot_daily
from graphs.graph_daily_activity_multiple import graph_daily_activity_multiple
from graphs.graph_line_online_counter import graph_line_online_counter
from graphs.graph_avg_time_by_platform import graph_avg_time_by_platform
from graphs.graph_avg_median import graph_avg_median

from utils.save_platforms import save_platforms
from utils.save_users import save_users

class Ui_MainWindow(object):
    '''
    Класс, описывающий главное окно программы и логику его работы

    Автор
    -----
    Илья Абрамов, Иван Чеканов, Яна Евдокимова, Егор Волков
    '''
    def lock_ui(func):
        '''
        Декоратор, запрещающий изменение базы данных во время выбора настроек 
        создания графика или текстового отчёта.

        Автор
        -----
        Иван Чеканов
        '''        
        def wrapper(self):
            self.pushButton.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            self.tab_4.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tab_5.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tab_6.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            return_value = func(self)
            self.tab_4.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
            self.tab_5.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
            self.tab_6.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
            self.pushButton.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            return return_value
        return wrapper

    
    def Report1(self):
        '''
        Метод создания текстового отчёта "Список сессий за выбранный период"

        Автор
        -----
        Илья Абрамов
        '''
        self.textReport1 = TextReport1(self.db_session, self.connection, self.ui1.selected_users, self.ui1.dateEdit.dateTime().toPyDateTime(), self.ui1.dateEdit_2.dateTime().toPyDateTime())
        self.textReport1.resizeColumnsToContents()
        self.scrollArea.setWidget(self.textReport1)
        self.statusbar.showMessage("Отчёт успешно создан.")


    def Report2(self):
        '''
        Метод создания текстового отчёта "Список активных пользователей за выбранный период"

        Автор
        -----
        Илья Абрамов
        '''
        self.textReport2 = TextReport2(self.db_session, self.ui1.dateEdit.dateTime().toPyDateTime(), self.ui1.dateEdit_2.dateTime().toPyDateTime())
        self.textReport2.resizeColumnsToContents()
        self.scrollArea.setWidget(self.textReport2)
        self.statusbar.showMessage("Отчёт успешно создан.")


    def Report3(self):
        '''
        Метод создания текстового отчёта "Сводная таблица"

        Автор
        -----
        Иван Чеканов
        '''
        self.textReport3 = TextReport3(self.db_session, self.ui1.selected_users, self.ui1.dateEdit.dateTime().toPyDateTime(), self.ui1.dateEdit_2.dateTime().toPyDateTime())
        self.scrollArea.setWidget(self.textReport3)
        self.statusbar.showMessage("Отчёт успешно создан.")


    def Graph(self, mode: int):
        '''
        Метод интеграции графического отчёта в интерфейс программы

        Параметры
        ---------
        mode : int
            Номер графика для создания
        
        Автор
        -----
        Илья Абрамов
        '''
        users = self.ui2.selected_users
        tstart = self.ui2.dateEdit.dateTime().toPyDateTime()
        tend = self.ui2.dateEdit_2.dateTime().toPyDateTime()

        if mode == 1:   w = GraphWidget(graph_bars_accumulated(self.db_session, users, tstart, tend))
        elif mode == 2: w = GraphWidget(graph_boxplot_daily(self.db_session, users, tstart, tend))
        elif mode == 3: w = GraphWidget(graph_daily_activity_multiple(self.db_session, users, tstart, tend))
        # elif mode == 4: w = GraphWidget(graph_histogram_sessions(self.db_session, tstart, tend))
        elif mode == 4: w = GraphWidget(graph_histogram_sessions_platforms(self.db_session, tstart, tend))
        elif mode == 5: w = GraphWidget(graph_line_online_counter(self.db_session, tstart, tend))
        elif mode == 6: w = GraphWidget(graph_scatter(self.db_session, tstart, tend))
        elif mode == 7: w = GraphWidget(graph_avg_time_by_platform(self.db_session, tstart, tend))
        elif mode == 8: w = GraphWidget(graph_avg_median(self.db_session, tstart, tend))
        elif mode == 9: w = GraphWidget(graph_bars_accumulated_by_platforms(self.db_session, users, tstart, tend))

        self.scrollAreaWidgetContents_3.close()
        self.scrollAreaWidgetContents_3.deleteLater()
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_3)
        self.scrollAreaWidgetContents_3.setLayout(w.layout)
        
        self.statusbar.showMessage("График успешно построен.")

    @lock_ui
    def dialog1ButtonClicked(self):
        '''
        Метод обработки нажатия кнопки "Создать текстовый отчёт"

        Автор
        -----
        Илья Абрамов, Иван Чеканов
        '''
        self.dialog1.show()
        self.dialog1.exec()
        if not self.dialog1.result():
            return
        if not self.ui1.dateEdit.dateTime() < self.ui2.dateEdit_2.dateTime():
            QtWidgets.QMessageBox().critical(self.centralwidget, "Ошибка", "Начальная дата больше конечной. Повторите попытку ввода.")
            return
        multiple_buttons = [self.ui1.radioButton.isChecked(), self.ui1.radioButton_2.isChecked()]
        if any(multiple_buttons) and not self.ui1.selected_users:
            QtWidgets.QMessageBox().critical(self.centralwidget, "Ошибка", "Не было выбрано ни одного пользователя. Повторите попытку ввода.")
            return
        if self.ui1.radioButton_2.isChecked():
            self.Report1()  # Список сессий для выбранных пользователей
        elif self.ui1.radioButton_3.isChecked():
            self.Report2()  # Список активных пользоватлей
        elif self.ui1.radioButton.isChecked():
            self.Report3()  # Количество сессий с платформ по пользователям (сводная таблица)
        else:
            QtWidgets.QMessageBox().critical(self.centralwidget, "Ошибка", "Не был выбран ни один графический отчёт. Повторите попытку ввода.")
            return
        self.tabWidget.setCurrentIndex(1)


    @lock_ui
    def dialog2ButtonClicked(self):
        '''
        Метод обработки нажатия кнопки "Создать графический отчёт"

        Автор
        -----
        Илья Абрамов, Иван Чеканов
        '''
        self.dialog2.show()
        self.dialog2.exec()
        if not self.dialog2.result():
            return
        if not self.ui2.dateEdit.dateTime() < self.ui2.dateEdit_2.dateTime():
            QtWidgets.QMessageBox().critical(self.centralwidget, "Ошибка", "Начальная дата больше конечной. Повторите попытку ввода.")
            return
        multiple_buttons = [
            self.ui2.radioButton_2.isChecked(), 
            self.ui2.radioButton_5.isChecked(), 
            self.ui2.radioButton_6.isChecked(),
            self.ui2.radioButton_9.isChecked()
        ]
        if any(multiple_buttons) and not self.ui2.selected_users:
            QtWidgets.QMessageBox().critical(self.centralwidget, "Ошибка", "Не было выбрано ни одного пользователя. Повторите попытку ввода.")
            return
        if self.ui2.radioButton_2.isChecked():
            self.Graph(1)  # Столбчатый график активности
        elif self.ui2.radioButton_5.isChecked():
            self.Graph(2)  # Бокс-Уискер
        elif self.ui2.radioButton_6.isChecked():
            self.Graph(3)  # Активность в течении одного для для пользователя
        elif self.ui2.radioButton_8.isChecked():
            self.Graph(4)  # Гистограмма
        elif self.ui2.radioButton_7.isChecked():
            self.Graph(5)  # График кол-ва пользователей в сети
        elif self.ui2.radioButton.isChecked():
            self.Graph(6)  # Диаграмма рассеивания
        elif self.ui2.radioButton_3.isChecked():
            self.Graph(7)  # Сравнение среднего времени по платформам
        elif self.ui2.radioButton_4.isChecked():
            self.Graph(8)  # Сравнение медианной и средней длительности
        elif self.ui2.radioButton_9.isChecked():
            self.Graph(9)  # Столбчатый график активности с платформами
        else:
            QtWidgets.QMessageBox().critical(self.centralwidget, "Ошибка", "Не был выбран ни один графический отчёт. Повторите попытку ввода.")
            return
        self.tabWidget.setCurrentIndex(2)


    def saveReport(self):
        '''
        Метод обработки нажатия кнопки "сохранить" для текстового отчёта

        Автор
        -----
        Иван Чеканов
        '''
        if not self.scrollArea.widget():
            QtWidgets.QMessageBox().critical(self.centralwidget, "Ошибка", "Чтобы сохранить что-нибудь ненужное, надо сначала сгенерировать что-нибудь ненужное. Пожалуйста, создайте отчёт, чтобы сохранить его.")
        try:
            if self.scrollArea.widget().saveReport(self.db_session):
                self.statusbar.showMessage("Отчёт успешно сохранён.")
            else:
                self.statusbar.showMessage("Не был выбран файл.")
        except AttributeError:
            self.statusbar.showMessage("Проблема при сохранении отчёта.")


    def addRecordBtnClicked(self):
        '''
        Метод добавления строки в базу данных

        Автор
        -----
        Илья Абрамов
        '''
        if self.tabWidget_2.currentIndex() == 0:
            r = self.model1.record()
            r.setValue("name", "Username_" + str(self.model1.rowCount() + 1))
            r.setValue("vk_id", self.model1.rowCount() + 1)
            r.setValue("university_group", None)
            self.model1.insertRecord(-1, r)
            self.model1.select()
        elif self.tabWidget_2.currentIndex() == 1:
            r = self.model2.record()
            n = self.model2.rowCount()+1
            r.setValue("slug", f"SLUG_{str(n)}")
            r.setValue("description", f"DESCRIPTION_{n}")
            self.model2.insertRecord(-1, r)
            self.model2.select()
        elif self.tabWidget_2.currentIndex() == 2:
            r = self.model3.record()
            r.setValue("user_id", 0)
            time = QtCore.QDateTime.currentDateTime()
            r.setValue("session_start", time)
            r.setValue("session_end", time)
            r.setValue("platform_id", 0)
            self.model3.insertRecord(-1, r)
            self.model3.select()
        self.statusbar.showMessage("Строка успешно добавлена.")
        
    
    def deleteSelectedRows(self):
        '''
        Метод удаления строки из базы данных

        Автор
        -----
        Иван Чеканов
        '''
        opened_tab_index = self.tabWidget_2.currentIndex()
        current_tab = [self.tab_4, self.tab_5, self.tab_6][opened_tab_index]
        current_model = [self.model1, self.model2, self.model3][opened_tab_index]
        indices = current_tab.selectionModel().selectedRows() 
        for index in sorted(indices):
            current_model.removeRow(index.row()) 
        n = len(indices)
        if n == 0:
            QtWidgets.QMessageBox().critical(self.centralwidget, "Ошибка", "Не выбрано ни одной строки.")
        elif n == 1:
            self.statusbar.showMessage("Успешно удалена 1 строка.")
        else:
            word = "строки" if n in (2,3,4) else "строк"
            self.statusbar.showMessage(f"Успешно удалено {n} {word}.")


    def dataBases(self, *args):
        '''
        Метод получения данных из базы данных для заполнения графического интерфейса программы

        Автор
        -----
        Илья Абрамов
        '''
        self.connection = QSqlDatabase.addDatabase("QSQLITE")
        self.connection.setDatabaseName(self.filepath)
        self.connection.open()

        self.model1 = QSqlTableModel()
        self.model1.setTable("user")
        self.model1.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model1.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        self.model1.setHeaderData(1, QtCore.Qt.Horizontal, "Name")
        self.model1.setHeaderData(2, QtCore.Qt.Horizontal, "VK id")
        self.model1.setHeaderData(3, QtCore.Qt.Horizontal, "Group")
        self.model1.select()

        if not self.model1.rowCount():
            self.connection.close()
            return False

        self.tab_4 = QtWidgets.QTableView()
        self.tab_4.setModel(self.model1)
        self.tab_4.resizeColumnsToContents()
        self.tab_4.setColumnWidth(2, 100)
        self.tab_4.setColumnWidth(3, 100)

        self.model2 = QSqlTableModel()
        self.model2.setTable("platform")
        self.model2.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model2.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        self.model2.setHeaderData(1, QtCore.Qt.Horizontal, "Slug")
        self.model2.setHeaderData(2, QtCore.Qt.Horizontal, "Description")
        self.model2.select()

        self.tab_5 = QtWidgets.QTableView()
        self.tab_5.setModel(self.model2)
        self.tab_5.resizeColumnsToContents()

        self.model3 = QSqlTableModel()
        self.model3.setTable("activity")
        self.model3.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model3.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        self.model3.setHeaderData(1, QtCore.Qt.Horizontal, "User id")
        self.model3.setHeaderData(2, QtCore.Qt.Horizontal, "Session start")
        self.model3.setHeaderData(3, QtCore.Qt.Horizontal, "Session end")
        self.model3.setHeaderData(4, QtCore.Qt.Horizontal, "Platform id")
        self.model3.select()

        self.tab_6 = QtWidgets.QTableView()
        self.tab_6.setModel(self.model3)
        self.tab_6.sortByColumn(0, QtCore.Qt.DescendingOrder)  # Qt.DescendingOrder Qt.AscendingOrder
        self.tab_6.resizeColumnsToContents()
        
        return True

        
    def openDB(self, MainWindow: QtWidgets.QMainWindow):
        '''
        Метод инициализации баз данных QT и SQLAlchemy

        Параметры
        ---------
        MainWindow : QtWidgets.QMainWindow
            Объект главного окна программы

        Автор
        -----
        Иван Чеканов
        '''
        self.filepath = QtWidgets.QFileDialog().getOpenFileName(filter="База данных (*.db *.sqlite *.sqlite3)")[0]
        # self.filepath = "C:\\Users\\is-20\\Documents\\GitHub\\vk_online_analysis\\data\\project.db"
        if not self.filepath:
            return
        if not self.dataBases(MainWindow):
            QtWidgets.QMessageBox().critical(
                self.centralwidget, "Ошибка", "Структура выбранной базы данных не соответствует требуемой для работы программы. Выберите другую базу данных.")
            return
        engine = create_engine(f"sqlite:///{self.filepath}")
        self.db_session = sessionmaker(engine)()
        # setting up the UI
        self.statusbar.showMessage("Подключение к базе данных выполнено успешно.")
        self.action.triggered.disconnect()
        self.action.triggered.connect(lambda: QtWidgets.QMessageBox().warning(
            self.centralwidget, "Предупреждение", "База данных уже выбрана. Чтобы сменить базу данных перезапустите приложение."))
        self.ui2.setupUi(self.dialog2, self, self.connection)
        self.ui1.setupUi(self.dialog1, self, self.connection)
        self.tab_4.setObjectName("tab_4")
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_5.setObjectName("tab_5")
        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_6.setObjectName("tab_6")
        self.tabWidget_2.addTab(self.tab_6, "")
        _translate = QtCore.QCoreApplication.translate
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "Пользователи"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("MainWindow", "Платформы"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), _translate("MainWindow", "Активность"))
        self.action_7.setEnabled(True)
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.action_3.setEnabled(True)
        self.action_5.setEnabled(True)
        self.action_7.setEnabled(True)
        self.action_8.setEnabled(True)
        self.action_11.setEnabled(True)
        self.action_12.setEnabled(True)


    def btnClickSaveUsers(self, *args):
        '''
        Метод обработки нажатия кнопки "Сохранить список пользователей"

        Автор
        -----
        Илья Абрамов, Иван Чеканов
        '''
        if self.connection:
            save_users(self.db_session)
            self.statusbar.showMessage("Список пользователей успешно сохранён.")
        else:
            QtWidgets.QMessageBox().critical(self.centralwidget, "Ошибка", "Невозможно выполнить сохранение. Сначала откройте базу данных.")


    def btnClickSavePlatforms(self, *args):
        '''
        Метод обработки нажатия кнопки "Сохранить список платформ"

        Автор
        -----
        Илья Абрамов, Иван Чеканов
        '''
        if self.connection:
            save_platforms(self.db_session)
            self.statusbar.showMessage("Список платформ успешно сохранён.")
        else:
            QtWidgets.QMessageBox().critical(self.centralwidget, "Ошибка", "Невозможно выполнить сохранение. Сначала откройте базу данных.")


    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        '''
        Метод инициализации интерфейса диалога выбора пользователей

        Автор
        -----
        Илья Абрамов, Яна Евдокимова, Иван Чеканов
        '''
        self.connection = None
        self.GraphLayout = None

        self.dialog1 = QtWidgets.QDialog()
        self.ui1 = Ui_Dialog1()

        self.dialog2 = QtWidgets.QDialog()
        self.ui2 = Ui_Dialog2()
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(775, 652)
        MainWindow.showMaximized()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.verticalLayout_2.addWidget(self.tabWidget_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.pushButton = QtWidgets.QPushButton(self.tab)  # Добавить новую строку
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.addRecordBtnClicked)  # Установка триггера кнопки
        self.pushButton.setDisabled(True)
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab)  # Удалить строки
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.deleteSelectedRows)  # Установка триггера кнопки
        self.pushButton_4.setDisabled(True)
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()  # Текстовые отчёты
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.verticalLayout_7.addWidget(self.scrollArea)
        self.verticalLayout_5.addLayout(self.verticalLayout_7)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)  # Сгенерировать текстовый отчёт
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.dialog1ButtonClicked)
        self.pushButton_2.setDisabled(True)
        self.verticalLayout_5.addWidget(self.pushButton_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()  # Графические отчёты
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.tab_3)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 630, 442))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_8.addWidget(self.scrollArea_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_8)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_3)  # Построить график
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.dialog2ButtonClicked)
        self.pushButton_3.setDisabled(True)
        self.verticalLayout_4.addWidget(self.pushButton_3)
        self.tabWidget.addTab(self.tab_3, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 775, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action.triggered.connect(self.openDB)
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_3.setDisabled(True)
        self.action_3.triggered.connect(self.dialog1ButtonClicked)
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.setObjectName("action_5")  # Сохранить отчёт
        self.action_5.triggered.connect(self.saveReport)
        self.action_5.setDisabled(True)
        self.action_7 = QtWidgets.QAction(MainWindow)
        self.action_7.setObjectName("action_7")
        self.action_7.setDisabled(True)
        self.action_7.triggered.connect(lambda: self.statusbar.showMessage("База данных успешно сохранена."))
        self.action_8 = QtWidgets.QAction(MainWindow)
        self.action_8.setObjectName("action_8")
        self.action_8.setDisabled(True)
        self.action_8.triggered.connect(self.dialog2ButtonClicked)
        self.action_11 = QtWidgets.QAction(MainWindow)
        self.action_11.setObjectName("action_11")
        self.action_11.triggered.connect(self.btnClickSaveUsers)
        self.action_11.setDisabled(True)
        self.action_12 = QtWidgets.QAction(MainWindow)
        self.action_12.setObjectName("action_12")
        self.action_12.triggered.connect(self.btnClickSavePlatforms)
        self.action_12.setDisabled(True)
        self.menu.addAction(self.action)
        self.menu.addSeparator()
        self.menu.addAction(self.action_7)
        self.menu.addAction(self.action_11)
        self.menu.addAction(self.action_12)
        self.menu_2.addAction(self.action_3)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action_5)
        self.menu_3.addAction(self.action_8)
        self.menu_3.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        '''
        Метод добавления подписей к элементам интерфейса

        Автор
        -----
        Яна Евдокимова
        '''
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowIcon(QtGui.QIcon('ui/logo.png'))
        MainWindow.setWindowTitle(_translate("MainWindow", "Анализ активности ВК"))
        self.pushButton.setText(_translate("MainWindow", "Добавить новую строку"))
        self.pushButton_4.setText(_translate("MainWindow", "Удалить выбранные строки"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Просмотр/редактирование БД"))
        self.pushButton_2.setText(_translate("MainWindow", "Сгенерировать"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Текстовые отчёты"))
        self.pushButton_3.setText(_translate("MainWindow", "Построить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Графические отчёты"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainWindow", "Отчёт"))
        self.menu_3.setTitle(_translate("MainWindow", "График"))
        self.action.setText(_translate("MainWindow", "Открыть базу данных"))
        self.action_3.setText(_translate("MainWindow", "Сгенерировать"))
        self.action_5.setText(_translate("MainWindow", "Сохранить отчёт"))
        self.action_7.setText(_translate("MainWindow", "Сохранить базу данных"))
        self.action_8.setText(_translate("MainWindow", "Построить"))
        self.action_11.setText(_translate("MainWindow", "Сохранить список пользователей в файл"))
        self.action_12.setText(_translate("MainWindow", "Сохранить список платформ в файл"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
