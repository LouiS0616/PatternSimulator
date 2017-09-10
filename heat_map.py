from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QMouseEvent

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class _PlotCanvas(FigureCanvas):
    clicked = pyqtSignal()

    def __init__(self, parent: QObject=None):
        self._fig = Figure()
        self._axes = self._fig.add_subplot(1, 1, 1)
        self._heat_map = self._axes.pcolor([[]])

        FigureCanvas.__init__(self, self._fig)
        self.setParent(parent)

    @pyqtSlot(object)
    def plot(self, data) -> None:
        self._axes.pcolor(data)
        self.draw()

    def mousePressEvent(self, _: QMouseEvent) -> None:
        self.clicked.emit()


class HeatMapDialog(QDialog):
    def __init__(self, plotter):
        super(QDialog, self).__init__()

        self.my_plot = _PlotCanvas(self)
        self.show()

        self.plotter = plotter

        # noinspection PyUnresolvedReferences
        self.my_plot.clicked.connect(self.plotter.re_plot)
        self.plotter.data_ready.connect(self.my_plot.plot)

        self.thread = QThread()
        self.plotter.moveToThread(self.thread)
        self.thread.start()

        self.my_plot.clicked.emit()
