import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar


class GraphWidget(QtWidgets.QMainWindow):
    '''
    Класс, описывающий представление графика внутри главного окна программы

    Автор
    -----
    Илья Абрамов
    '''
    def __init__(self, figure):
        super(GraphWidget, self).__init__()
        self.fig = figure

        self.canvas = FigureCanvasQTAgg(self.fig)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

        self.show()