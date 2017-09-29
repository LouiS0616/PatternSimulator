import numpy as np

from model.formula import FormulaModel
from model.plotter.abstract_plotter import Plotter

from MyPyUtil.my_util import connect

from PyQt5.QtCore import pyqtSignal


class FormulaPlotter(Plotter):
    success_to_compute = pyqtSignal()
    error_occurred = pyqtSignal(str)

    request_for_exit = pyqtSignal(int)

    def __init__(self, model: FormulaModel, parent=None,
                 x_range: tuple=(-5., 5.), y_range: tuple=(-5., 5),
                 particle_num: int=64, auto_update: bool=True):

        Plotter.__init__(self, parent)
        self._model = model

        self._x_elements = np.linspace(*x_range, particle_num)
        self._y_elements = np.linspace(*y_range, particle_num)
        self._previous_z_elements = None

        self._num_of_error_occurrence_in_serial = 0

        if auto_update:
            connect(model.formula_updated, self.re_plot)

    def make_data(self) -> np.ndarray:
        formula_instance = \
            self._model.get_substituted_formula_except_xy()

        z_elements = [
            [formula_instance.subs([('x', x), ('y', y)]) for x in self._x_elements]
            for y in self._y_elements
        ]

        try:
            ret = np.array(z_elements, dtype=np.float64)
        except TypeError:
            self._report_result(False, 'Complex value or division-by-zero might occur.')
            return self._previous_z_elements

        self._previous_z_elements = ret
        self._report_result(True)
        return ret

    def _report_result(self, result: bool, text: str=''):
        if result:
            self._num_of_error_occurrence_in_serial = 0
            self.success_to_compute.emit()
        else:
            self._num_of_error_occurrence_in_serial += 1

            if self._num_of_error_occurrence_in_serial >= 4:
                self.request_for_exit.emit(1)
                return

            self.error_occurred.emit(text)
