from model.formula import FormulaModel
from model.plotter.formula_plotter import FormulaPlotter
from view.heat_map import PlotCanvas

from PyQt5.QtCore import QObject, pyqtSlot


class PlotSaver(QObject):
    def __init__(self, model: FormulaModel, particle_num: int=64, parent=None):
        QObject.__init__(self, parent)
        self._plotter = FormulaPlotter(model, particle_num=particle_num, auto_update=False)
        self._plot_canvas = PlotCanvas()

    @pyqtSlot(str)
    def save_fig(self, name: str) -> None:
        print('Start to save ' + name + ' ...')
        self._plotter.re_plot()
        self._plot_canvas.plot(self._plotter.make_data())
        self._plot_canvas.save_fig(name)
        print('Save finished.')