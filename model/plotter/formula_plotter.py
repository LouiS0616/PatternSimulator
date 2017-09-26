import numpy as np

from model.formula import FormulaModel
from model.plotter.abstract_plotter import Plotter

from MyPyUtil.my_util import connect


class FormulaPlotter(Plotter):
    def __init__(self, model: FormulaModel, parent=None,
                 x_range: tuple=(-5., 5.), y_range: tuple=(-5., 5),
                 particle_num: int=64):

        Plotter.__init__(self, parent)
        self._model = model

        self._x_elements = np.linspace(*x_range, particle_num)
        self._y_elements = np.linspace(*y_range, particle_num)

        connect(model.formula_updated, self.re_plot)

    def make_data(self) -> np.ndarray:
        formula_instance = \
            self._model.get_substituted_formula_except_xy()

        z_elements = [
            [formula_instance.subs([('x', x), ('y', y)]) for x in self._x_elements]
            for y in self._y_elements
        ]
        return np.array(z_elements, dtype=np.float64)
