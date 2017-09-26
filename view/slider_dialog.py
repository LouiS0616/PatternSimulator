from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QWidget
from PyQt5.QtGui import QFont

from FloatSlider.slider import FloatSliderWithEditor
from MyPyUtil.my_util.qt_util import connect


class SliderDialog(QDialog):
    item_changed = pyqtSignal(str, float)

    def __init__(self):
        QDialog.__init__(self, parent=None)
        self._layout = QFormLayout()

    def add_row(self, name: str) -> None:
        label = MyLabel(name, self)
        slider = FloatSliderWithEditor()
        connect(slider.valueChanged, label.slider_changed)

        self._layout.addRow(label, slider)
        self.setLayout(self._layout)
        connect(label.item_changed, self.item_changed)


class MyLabel(QLabel):
    item_changed = pyqtSignal(str, float)
    font = QFont('consolas')

    def __init__(self, text: str, parent):
        QLabel.__init__(self, text=text, parent=parent)
        self._text = text

        self.setFont(self.font)
        self.setAlignment(Qt.AlignBottom)

    @pyqtSlot(float)
    def slider_changed(self, value: float):
        self.item_changed.emit(self._text, value)
