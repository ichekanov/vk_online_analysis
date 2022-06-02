# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from ui.ChooseUsers import ChooseUsers_Dialog

class Ui_Dialog(object):
    '''
    Класс, описывающий диалог параметров графического отчёта

    Автор
    -----
    Илья Абрамов
    '''
    def openChooseUsers(self):
        '''
        Метод, запускающий окно выбора пользователей для отображения на графике

        Автор
        -----
        Илья Абрамов
        '''
        self.ui.fill_list()
        self.dialog.show()
        self.dialog.exec()
        if self.dialog.result() == 1:
            # print(f"{self.ui.selected_users=}")
            self.selected_users = self.ui.selected_users

    def setupUi(self, Dialog: QtWidgets.QDialog, MainWindow, connection):
        '''
        Метод инициализации интерфейса диалога выбора пользователей

        Автор
        -----
        Илья Абрамов, Яна Евдокимова
        '''
        self.connection = connection
        self.dialog = QtWidgets.QDialog()
        self.ui = ChooseUsers_Dialog()
        self.ui.setupUi(self.dialog, self, self.connection)
        self.selected_users = set()

        Dialog.setObjectName("Dialog")
        # Dialog.resize(524, 200)
        Dialog.setWindowIcon(QtGui.QIcon('ui/logo.png'))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.dateEdit = QtWidgets.QDateTimeEdit(Dialog)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDateTime(QtCore.QDateTime(2022, 3, 17, 0, 0, 0, 0))  # Базовое время
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setMinimumDate(QtCore.QDate(2022, 3, 16))
        self.dateEdit.setMaximumDate(QtCore.QDate(2022, 6, 1))
        self.verticalLayout.addWidget(self.dateEdit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.dateEdit_2 = QtWidgets.QDateTimeEdit(Dialog)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.dateEdit_2.setDateTime(QtCore.QDateTime(2022, 3, 18, 0, 0, 0, 0))  # Базовое время
        self.dateEdit_2.setCalendarPopup(True)
        self.dateEdit_2.setMinimumDate(QtCore.QDate(2022, 3, 16))
        self.dateEdit_2.setMaximumDate(QtCore.QDate(2022, 6, 1))
        self.verticalLayout.addWidget(self.dateEdit_2)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openChooseUsers)
        self.verticalLayout.addWidget(self.pushButton)
        self.lineSpacer1 = QtWidgets.QFrame(Dialog)
        self.lineSpacer1.setFrameShape(QtWidgets.QFrame.HLine)
        self.lineSpacer1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineSpacer1.setObjectName("lineSpacer1")
        self.verticalLayout.addWidget(self.lineSpacer1)

        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        # self.label_4 = QtWidgets.QLabel(Dialog)
        # self.label_4.setObjectName("label_4")
        # self.verticalLayout.addWidget(self.label_4)
        # self.pushButton = QtWidgets.QPushButton(Dialog)
        # self.pushButton.setObjectName("pushButton")
        # self.pushButton.clicked.connect(self.openChooseUsers)
        # self.verticalLayout.addWidget(self.pushButton)
        self.radioButton_5 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_5.setObjectName("radioButton_5")
        self.verticalLayout.addWidget(self.radioButton_5)
        # self.label_3 = QtWidgets.QLabel(Dialog)
        # self.label_3.setObjectName("label_3")
        # self.verticalLayout.addWidget(self.label_3)
        # self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        # self.pushButton_2.setObjectName("pushButton_2")
        # self.pushButton_2.clicked.connect(self.openChooseUsers)
        # self.verticalLayout.addWidget(self.pushButton_2)
        self.radioButton_6 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_6.setObjectName("radioButton_6")
        self.verticalLayout.addWidget(self.radioButton_6)
        # self.label_6 = QtWidgets.QLabel(Dialog)
        # self.label_6.setObjectName("label_6")
        # self.verticalLayout.addWidget(self.label_6)
        # self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        # self.pushButton_3.setObjectName("pushButton_3")
        # self.pushButton_3.clicked.connect(self.openChooseUsers)
        # self.verticalLayout.addWidget(self.pushButton_3)
        self.radioButton_8 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_8.setObjectName("radioButton_8")
        self.verticalLayout.addWidget(self.radioButton_8)
        self.radioButton_7 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_7.setObjectName("radioButton_7")
        self.verticalLayout.addWidget(self.radioButton_7)
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_3 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout.addWidget(self.radioButton_3)
        # self.label_5 = QtWidgets.QLabel(Dialog)
        # self.label_5.setObjectName("label_5")
        # self.verticalLayout.addWidget(self.label_5)
        # self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        # self.pushButton_4.setObjectName("pushButton_4")
        # self.pushButton_4.clicked.connect(self.openChooseUsers)  # Тут должен быть выбор платформ
        # self.verticalLayout.addWidget(self.pushButton_4)
        self.radioButton_4 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_4.setObjectName("radioButton_4")
        self.verticalLayout.addWidget(self.radioButton_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        '''
        Метод добавления подписей к элементам интерфейса

        Автор
        -----
        Яна Евдокимова
        '''
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Создание графического отчёта"))
        self.label.setText(_translate("Dialog", "Укажите начало периода:"))
        self.label_2.setText(_translate("Dialog", "Укажите конец периода:"))
        self.radioButton_2.setText(_translate("Dialog", "Суммарная длительность сессий выбранных пользователей"))
        self.label_4.setText(_translate("Dialog", "Выберите пользователей:"))
        self.pushButton.setText(_translate("Dialog", "Открыть таблицу"))
        self.radioButton_5.setText(_translate("Dialog", "«Ящик с усами» для времени в сети выбранных пользователей, сгруппированного по дням"))
        # self.label_3.setText(_translate("Dialog", "Выберите пользователей:"))
        # self.pushButton_2.setText(_translate("Dialog", "Открыть таблицу"))
        self.radioButton_6.setText(_translate("Dialog", "Активность выбранных пользователей (длительность сессий)"))
        # self.label_6.setText(_translate("Dialog", "Выберите пользователя:"))
        # self.pushButton_3.setText(_translate("Dialog", "Открыть таблицу"))
        self.radioButton_8.setText(_translate("Dialog", "Распределение числа сессий по длительности"))
        self.radioButton_7.setText(_translate("Dialog", "График суммарного количества пользователей в сети"))
        self.radioButton.setText(_translate("Dialog", "Длительность сессий в зависимости от времени"))
        self.radioButton_3.setText(_translate("Dialog", "Сравнение среднего времени по платформам"))
        # self.label_5.setText(_translate("Dialog", "Выберите платформы:"))
        # self.pushButton_4.setText(_translate("Dialog", "Открыть таблицу"))s
        self.radioButton_4.setText(_translate("Dialog", "Средняя и медианная длительность сессии в зависимости от времени"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
