# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChooseUsers.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlQuery


class ChooseUsers_Dialog(object):
    '''
    Класс, описывающий диалог выбора пользователей

    Автор
    -----
    Илья Абрамов
    '''
    def addUser(self, *args):
        '''
        Метод для добавление пользователей в список "выбранные"

        Автор
        -----
        Илья Абрамов
        '''
        # print(self.listWidget.currentItem().text(), self.users[self.listWidget.currentItem().text()])
        if self.users[self.listWidget.currentItem().text()] not in self.selected_users:
            self.selected_users.add(self.users[self.listWidget.currentItem().text()])
            t = QtWidgets.QListWidgetItem(self.listWidget_2)
            t.setText(self.listWidget.currentItem().text())


    def deleteUser(self, listItem):
        '''
        Метод для удаления пользователей из списка "выбранные"

        Автор
        -----
        Илья Абрамов
        '''
        if self.users[self.listWidget_2.currentItem().text()] in self.selected_users:
            self.selected_users.remove(self.users[self.listWidget_2.currentItem().text()])
            self.listWidget_2.removeItemWidget(listItem)
            self.listWidget_2.takeItem(self.listWidget_2.row(listItem))


    def fill_list(self):
        '''
        Метод для заполнения списка пользователей данными из БД

        Автор
        -----
        Илья Абрамов
        '''
        Users = QSqlQuery()
        Users.exec(
            """
            SELECT * FROM user
            """
        )
        self.users = {}
        self.listWidget.clear()
        while Users.next():
            self.users.update({Users.value(1) : Users.value(0)}) # name: id
            t = QtWidgets.QListWidgetItem(self.listWidget)
            t.setText(Users.value(1))
    

    def clear_all_selected(self, *args):
        self.selected_users = set()
        self.listWidget_2.clear()
    

    def setupUi(self, Dialog: QtWidgets.QDialog, MainWindow, connection):
        '''
        Метод инициализации интерфейса диалога выбора пользователей

        Автор
        -----
        Илья Абрамов, Яна Евдокимова
        '''
        self.selected_users = set()
        self.mainwindow = MainWindow
        self.connection = connection

        Dialog.setObjectName("Dialog")
        Dialog.resize(484, 351)
        Dialog.setMinimumSize(QtCore.QSize(484, 351))
        Dialog.setWindowIcon(QtGui.QIcon('ui/logo.png'))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(390, 240, 81, 91))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Reset|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setEnabled(True)
        self.listWidget.setGeometry(QtCore.QRect(20, 20, 171, 301))
        self.fill_list()
        self.listWidget.itemDoubleClicked.connect(self.addUser)
        self.listWidget.setObjectName("listWidget")
        self.listWidget_2 = QtWidgets.QListWidget(Dialog)
        self.listWidget_2.setEnabled(True)
        self.listWidget_2.setGeometry(QtCore.QRect(200, 20, 171, 301))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.itemDoubleClicked.connect(self.deleteUser)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.clear_all_selected)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        '''
        Метод добавления подписей к элементам интерфейса

        Автор
        -----
        Яна Евдокимова
        '''
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Выберите пользователей"))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).setText(_translate("Dialog", "Очистить"))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(_translate("Dialog", "Отмена"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
