from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QMouseEvent

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class HeatMapDialog(QDialog):
    should_be_updated = pyqtSignal()

    def __init__(self, plotter, parent=None):
        QDialog.__init__(self, parent)

        self.my_plot = _PlotCanvas(self)
        self.show()

        self.plotter = plotter

        # noinspection PyUnresolvedReferences
        self.should_be_updated.connect(
            self.plotter.re_plot
        )
        self.plotter.data_ready.connect(
            self.my_plot.plot
        )

        self.thread = QThread()
        self.plotter.moveToThread(self.thread)
        self.thread.start()

        self.should_be_updated.emit()


class _PlotCanvas(FigureCanvas):
    clicked = pyqtSignal()

    def __init__(self, parent: HeatMapDialog):
        self._fig = Figure()
        self._axes = self._fig.add_subplot(1, 1, 1)
        self._heat_map = self._axes.pcolor([[]])

        FigureCanvas.__init__(self, self._fig)
        self.setParent(parent)

        self.clicked.connect(parent.should_be_updated)

    @pyqtSlot(object)
    def plot(self, data) -> None:
        # noinspection PyUnresolvedReferences
        self._axes.pcolor(data, cmap=plt.cm.PuOr)
        self.draw()

    def mousePressEvent(self, _: QMouseEvent) -> None:
        self.clicked.emit()
