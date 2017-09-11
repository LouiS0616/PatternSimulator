from heat_map import HeatMapDialog
from AbstractPlotter import Plotter

from PyQt5.QtWidgets import QApplication

import sys
import numpy as np


class MyPlotter(Plotter):
    def __init__(self, parent=None):
        Plotter.__init__(self, parent)

    def make_data(self) -> np.ndarray:
        return np.random.rand(12, 12)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plotter = MyPlotter()
    win = HeatMapDialog(plotter)
    print('multi')
    sys.exit(app.exec_())
