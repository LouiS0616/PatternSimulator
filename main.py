import sys
from datetime import datetime

import sympy as sp
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QApplication
from sympy import symbols

from model.formula import FormulaModel
from model.plotter.formula_plotter import FormulaPlotter
from view.heat_map import HeatMapDialog
from plot_saver import PlotSaver

from view.slider_dialog import SliderDialog
from FloatSlider.slider.float_slider_with_editor import FloatSliderWithEditor

from MyPyUtil.my_util.qt_util import connect


class Main(QObject):
    save_name_decided = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self, parent=None)
        self.app = QApplication(sys.argv)

        x, y = symbols('x y')

        """---- HERE TO REWRITE FORMULA ----"""
        a, b, c = symbols('kill survive param3')
        self._formula = a*sp.sin(x) + b*sp.tanh(y) + (c**(1./2.))*x
        """---------------------------------"""

        self._model = FormulaModel(self._formula)
        self._plotter = FormulaPlotter(self._model, particle_num=32)
        connect(self._plotter.error_occurred, self.output_error_log)

        """ HERE TO INITIALIZE COEFFICIENTS """
        self._model.set_a_coefficient_value('kill', 3)
        self._model.set_a_coefficient_value('survive', 3)
        self._model.set_a_coefficient_value('param3', 4)
        """---------------------------------"""

        # Heat Map Dialog
        self._win = HeatMapDialog(self._plotter)
        self._win.setWindowTitle('Pattern Simulator (C) Loui Sakaki 2017')
        connect(self._win.canvas.clicked, self.make_name_to_save)
        connect(self._win.finished, self._quit)

        # Plot Saver
        self._plot_saver = PlotSaver(self._model)
        self._save_thread = QThread()
        self._plot_saver.moveToThread(self._save_thread)
        self._save_thread.start()
        connect(self.save_name_decided, self._plot_saver.save_fig)

        # Sliders Dialog
        self._slider_dialog = SliderDialog()
        coefficient_dict = self._model.coefficient_dict

        for param in self._model.get_coefficient_list():
            slider_with_editor = FloatSliderWithEditor()
            slider_with_editor.slider.set_initial_value(coefficient_dict[param])
            slider_with_editor.slider.set_value(coefficient_dict[param])
            slider_with_editor.slider.set_range(-20., 20.)
            self._slider_dialog.add_row(name=param, slider_with_editor=slider_with_editor)

        connect(self._slider_dialog.item_changed, self.slot_item_changed)
        connect(self._slider_dialog.request_for_save, self.make_name_to_save)

        connect(self._plotter.success_to_compute, self._slider_dialog.save_values)

        # Adjust window position
        self._win.move(160, 124)
        self._slider_dialog.move(
            self._win.pos().x() + self._win.size().width() + 10,
            self._win.pos().y() + self._win.size().height() - self._slider_dialog.sizeHint().height()
        )
        self._slider_dialog.show()
        self._win.show()

        sys.exit(self.app.exec_())

    @pyqtSlot(str)
    def output_error_log(self, message) -> None:
        with open('result/error_log.txt', 'a') as f:
            def write(arg=''):
                f.write(arg + '\n')
                print(arg)

            f.write('-' * 64 + '\n')
            f.write(str(datetime.today()) + '\n')
            write(message)
            write(str(self._model))
            write(str(self._model.coefficient_dict))
            write()

        self._slider_dialog.load_values()

    @pyqtSlot()
    def make_name_to_save(self) -> None:
        names = []
        for name, value in self._slider_dialog.get_items():
            names.append(name + '=' + str(value))
        self.save_name_decided.emit(','.join(names))

    @pyqtSlot(str, float)
    def slot_item_changed(self, text: str, value: float):
        self._model.set_a_coefficient_value(text, value)

    @pyqtSlot(int)
    def _quit(self, _):
        self._save_thread.quit()
        self._win.thread.quit()
        self.app.quit()

if __name__ == '__main__':
    main = Main()
