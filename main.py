from heat_map import HeatMapDialog

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication

import sys
import numpy as np


class Plotter(QObject):
    data_ready = pyqtSignal(object)

    @pyqtSlot()
    def re_plot(self) -> None:
        data = np.random.rand(12, 12)
        self.data_ready.emit(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plotter = Plotter()
    win = HeatMapDialog(plotter)
    print('multi')
    sys.exit(app.exec_())
