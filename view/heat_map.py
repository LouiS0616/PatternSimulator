from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QMouseEvent

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from MyPyUtil.my_util.qt_util import connect


class HeatMapDialog(QDialog):
    should_be_updated = pyqtSignal()

    def __init__(self, plotter, parent=None):
        QDialog.__init__(self, parent)

        self._canvas = _PlotCanvas(self)
        self._plotter = plotter

        connect(
            self.should_be_updated,
            self._plotter.re_plot
        )
        connect(
            self._plotter.data_ready,
            self._canvas.plot
        )

        self._thread = QThread()
        self._plotter.moveToThread(self._thread)
        self._thread.start()

        self.should_be_updated.emit()
        self.show()

    @property
    def canvas(self) -> FigureCanvas:
        return self._canvas


class _PlotCanvas(FigureCanvas):
    clicked = pyqtSignal()

    # noinspection PyUnresolvedReferences
    color_map = plt.cm.PuOr

    def __init__(self, parent: HeatMapDialog):
        self._fig = Figure()
        self._axes = self._fig.add_subplot(1, 1, 1)

        FigureCanvas.__init__(self, self._fig)
        self.setParent(parent)

    @pyqtSlot(object)
    def plot(self, data) -> None:
        self._axes.pcolor(data, cmap=self.color_map)
        self.draw()

    def mousePressEvent(self, _: QMouseEvent) -> None:
        self.clicked.emit()

    def save_fig(self, name: str) -> None:
        self._fig.savefig(name + '.png')
