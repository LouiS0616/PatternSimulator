from float_slider import FloatSlider
from formula import FormulaModel

from PyQt5.QtWidgets import QDialog


class SliderDialog(QDialog):
    def __init__(self, model: FormulaModel, parent=None):
        QDialog.__init__(self, parent)
        self.variable_list = model.get_coefficient_list()
