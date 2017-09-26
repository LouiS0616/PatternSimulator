import sys

import sympy as sp
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication
from sympy import symbols

from model.formula import FormulaModel
from model.plotter.formula_plotter import FormulaPlotter
from view.heat_map import HeatMapDialog

from view.slider_dialog import SliderDialog


class Main(QObject):
    def __init__(self):
        QObject.__init__(self, parent=None)
        app = QApplication(sys.argv)

        x, y = symbols('x y')

        """---- HERE TO REWRITE FORMULA ----"""
        a, b, c = symbols('param1 param2 param3')
        self._formula = a*sp.sin(x) + b*sp.tanh(y) + c
        """---------------------------------"""

        self._model = FormulaModel(self._formula)
        self._plotter = FormulaPlotter(self._model, particle_num=32)

        """ HERE TO INITIALIZE COEFFICIENTS """
        self._model.set_a_coefficient_value('param1', 3)
        self._model.set_a_coefficient_value('param2', 3)
        self._model.set_a_coefficient_value('param3', 4)
        """---------------------------------"""

        self._win = HeatMapDialog(self._plotter)
        print('multi')

        self._slider_dialog = SliderDialog()
        for param in self._model.get_coefficient_list():
            self._slider_dialog.add_row(param)
        self._slider_dialog.show()

        sys.exit(app.exec_())

    @pyqtSlot(float)
    def slot_value_changed(self, value: float):
        print(value)
        self._model.set_a_coefficient_value('param1', value)


if __name__ == '__main__':
    main = Main()
