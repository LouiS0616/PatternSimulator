import sys

import sympy as sp
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication
from sympy import symbols

from model.formula import FormulaModel
from model.plotter.formula_plotter import FormulaPlotter
from view.heat_map import HeatMapDialog, PlotCanvas

from view.slider_dialog import SliderDialog
from FloatSlider.slider.float_slider_with_editor import FloatSliderWithEditor

from MyPyUtil.my_util.qt_util import connect


class Main(QObject):
    save_name_decided = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self, parent=None)
        app = QApplication(sys.argv)

        x, y = symbols('x y')

        """---- HERE TO REWRITE FORMULA ----"""
        a, b, c = symbols('kill survive param3')
        self._formula = a*sp.sin(x) + b*sp.tanh(y) + (c**(1./2.))*x
        """---------------------------------"""

        self._model = FormulaModel(self._formula)
        self._plotter = FormulaPlotter(self._model, particle_num=32)

        """ HERE TO INITIALIZE COEFFICIENTS """
        self._model.set_a_coefficient_value('kill', 3)
        self._model.set_a_coefficient_value('survive', 3)
        self._model.set_a_coefficient_value('param3', 4)
        """---------------------------------"""

        # Heat Map Dialog
        self._win = HeatMapDialog(self._plotter)
        connect(self._win.canvas.clicked, self.make_name_to_save)
        connect(self.save_name_decided, self._make_save_delicately(particle_num=128))
        self._win.show()

        # Sliders Dialog
        self._slider_dialog = SliderDialog()
        coefficient_dict = self._model.coefficient_dict

        for param in self._model.get_coefficient_list():
            slider_with_editor = FloatSliderWithEditor()
            slider_with_editor.slider.set_value(coefficient_dict[param])
            slider_with_editor.slider.set_range(-20., 20.)
            self._slider_dialog.add_row(name=param, slider_with_editor=slider_with_editor)

        connect(self._slider_dialog.item_changed, self.slot_item_changed)
        self._slider_dialog.show()

        sys.exit(app.exec_())

    @pyqtSlot()
    def make_name_to_save(self) -> None:
        names = []
        for name, value in self._slider_dialog.get_items():
            names.append(name + '=' + str(value))
        self.save_name_decided.emit(','.join(names))

    def _make_save_delicately(self, particle_num: int):
        _delicate_plotter = FormulaPlotter(self._model, particle_num=particle_num, auto_update=False)
        _delicate_figure = PlotCanvas()

        @pyqtSlot(str)
        def save_delicately(name: str) -> None:
            _delicate_plotter.re_plot()
            _delicate_figure.plot(_delicate_plotter.make_data())
            _delicate_figure.save_fig(name)

        return save_delicately

    @pyqtSlot(str, float)
    def slot_item_changed(self, text: str, value: float):
        self._model.set_a_coefficient_value(text, value)

if __name__ == '__main__':
    main = Main()
