import sys

import sympy as sp
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication
from sympy import symbols

from model.formula import FormulaModel
from model.plotter.formula_plotter import FormulaPlotter
from view.heat_map import HeatMapDialog

from view.slider_dialog import SliderDialog

from MyPyUtil.my_util.qt_util import connect


class Main(QObject):
    def __init__(self):
        QObject.__init__(self, parent=None)
        app = QApplication(sys.argv)

        x, y = symbols('x y')

        """---- HERE TO REWRITE FORMULA ----"""
        a, b, c = symbols('kill survive param3')
        self._formula = a*sp.sin(x) + b*sp.tanh(y) + c
        """---------------------------------"""

        self._model = FormulaModel(self._formula)
        self._plotter = FormulaPlotter(self._model, particle_num=32)

        """ HERE TO INITIALIZE COEFFICIENTS """
        self._model.set_a_coefficient_value('kill', 3)
        self._model.set_a_coefficient_value('survive', 3)
        self._model.set_a_coefficient_value('param3', 4)
        """---------------------------------"""

        self._win = HeatMapDialog(self._plotter)
        print('multi')

        self._slider_dialog = SliderDialog()
        for param in self._model.get_coefficient_list():
            self._slider_dialog.add_row(param)
        connect(self._slider_dialog.item_changed, self.slot_item_changed)
        self._slider_dialog.show()

        sys.exit(app.exec_())

    @pyqtSlot(str, float)
    def slot_item_changed(self, text: str, value: float):
        self._model.set_a_coefficient_value(text, value)


if __name__ == '__main__':
    main = Main()
