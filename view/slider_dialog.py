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
        self._rows = []

    def add_row(self, name: str) -> None:
        label = SliderDialog.MyLabel(name, self)
        slider = FloatSliderWithEditor()

        slider_changed = self._make_slider_changed(name)
        connect(slider.valueChanged, slider_changed)

        self._layout.addRow(label, slider)
        self.setLayout(self._layout)

    def _make_slider_changed(self, name: str):
        @pyqtSlot(float)
        def slider_changed(value: float):
            self.item_changed.emit(name, value)
        return slider_changed

    class MyLabel(QLabel):
        font = QFont('consolas')

        def __init__(self, text: str, parent: QWidget):
            QLabel.__init__(self, text=text, parent=parent)
            self.setFont(self.font)
            self.setAlignment(Qt.AlignBottom)
