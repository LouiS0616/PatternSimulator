import sympy
from sympy import symbols

from PyQt5.QtCore import QObject


class FormulaModel(QObject):
    def __init__(self, formula: sympy.add.Add, parent: QObject=None):
        QObject.__init__(self, parent)

        self._formula = formula
        self._coefficient_dict = \
            {name: 0 for name in map(str, self._formula.free_symbols)}

        # Remove variables
        self._coefficient_dict.pop('x', None)
        self._coefficient_dict.pop('y', None)

    def set_a_coefficient_value(self, key: str, value: float) -> None:
        self._coefficient_dict[key] = value

    def get_substituted_formula_except_xy(self) -> sympy.add.Add:
        substitute_list = list(zip(
            map(symbols, self._coefficient_dict.keys()),
            self._coefficient_dict.values()
        ))
        return self._formula.subs(substitute_list)

    def get_coefficient_list(self) -> list:
        return list(self._coefficient_dict.keys())