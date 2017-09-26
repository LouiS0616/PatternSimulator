import sys

import sympy as sp
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from sympy import symbols

from model.formula import FormulaModel
from model.plotter.formula_plotter import FormulaPlotter
from view.heat_map import HeatMapDialog

from FloatSlider.slider import FloatSliderWithEditor
from MyPyUtil.my_util import connect


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

        slider = FloatSliderWithEditor()
        connect(slider.valueChanged, self.slot_value_changed)
        slider.show()

        sys.exit(app.exec_())

    @pyqtSlot(float)
    def slot_value_changed(self, value: float):
        print(value)
        self._model.set_a_coefficient_value('param1', value)


class SliderDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, parent=None)


if __name__ == '__main__':
    main = Main()
