from heat_map import HeatMapDialog
from formula import FormulaModel

from formula_plotter import FormulaPlotter
from PyQt5.QtWidgets import QApplication

import sys
import sympy as sp
from sympy import symbols


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
    symbol_dict = model.coefficient_dict
    symbol_dict['param1'] = 3
    symbol_dict['param2'] = 3
    symbol_dict['param3'] = 4
    """---------------------------------"""

    win = HeatMapDialog(plotter)
    print('multi')
    sys.exit(app.exec_())
