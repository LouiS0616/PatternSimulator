from heat_map import HeatMapDialog
from formula import FormulaModel
from slider_dialog import SliderDialog

from formula_plotter import FormulaPlotter
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QSlider

import sys
import sympy as sp
from sympy import symbols


@pyqtSlot(float)
def slot_value_changed(value: float):
    print(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    x, y = symbols('x y')

    """---- HERE TO REWRITE FORMULA ----"""
    a, b, c = symbols('param1 param2 param3')
    formula = a*sp.sin(x) + b*sp.tanh(y) + c
    """---------------------------------"""

    model = FormulaModel(formula)
    plotter = FormulaPlotter(model)

    """ HERE TO INITIALIZE COEFFICIENTS """
    model.set_a_coefficient_value('param1', 3)
    model.set_a_coefficient_value('param2', 3)
    model.set_a_coefficient_value('param3', 4)
    """---------------------------------"""

    win = HeatMapDialog(plotter)
    print('multi')

    sys.exit(app.exec_())
