from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QSlider, QWidget


class FloatSlider(QWidget):
    value_changed = pyqtSignal(float)

    def __init__(self, callback_slot, s_digit: int=4, parent=None):
        QWidget.__init__(self, parent)

        self._slider = QSlider(parent=self)

        self._slider.setOrientation(Qt.Horizontal)
        # noinspection PyUnresolvedReferences
        self._slider.valueChanged.connect(self._slot_value_change)

        self.value_changed.connect(callback_slot)

    @pyqtSlot(int)
    def _slot_value_change(self):
        pass
