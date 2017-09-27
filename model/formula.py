import sympy
from sympy import symbols

from PyQt5.QtCore import QObject, pyqtSignal


class FormulaModel(QObject):
    formula_updated = pyqtSignal()

    def __init__(self, formula, parent: QObject=None):
        QObject.__init__(self, parent)

        self._formula = formula
        self._coefficient_dict = \
            {name: 0 for name in map(str, self._formula.free_symbols)}

        # Remove variables
        self._coefficient_dict.pop('x', None)
        self._coefficient_dict.pop('y', None)

    def set_a_coefficient_value(self, key: str, value: float) -> None:
        self._coefficient_dict[key] = value
        self.formula_updated.emit()

    def get_substituted_formula_except_xy(self) -> sympy.add.Add:
        substitute_list = list(zip(
            map(symbols, self._coefficient_dict.keys()),
            self._coefficient_dict.values()
        ))
        return self._formula.subs(substitute_list)

    def get_coefficient_list(self) -> list:
        return sorted(list(self._coefficient_dict.keys()))

    def __str__(self) -> str:
        return str(self._formula)

    @property
    def coefficient_dict(self) -> dict:
        return self._coefficient_dict
