import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Plotter(QObject):
    data_ready = pyqtSignal(object)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

    @pyqtSlot()
    def re_plot(self) -> None:
        data = self.make_data()
        self.data_ready.emit(data)

    def make_data(self) -> np.ndarray:
        pass


class PlotterSample(Plotter):
    def __init__(self, parent=None, grid: tuple=(12, 12)):
        Plotter.__init__(self, parent)
        self._grid = grid

    def make_data(self):
        return np.random.rand(*self._grid)

