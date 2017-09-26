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
        self._labels = []
        self._sliders = []

    def add_row(self, name: str) -> None:
        label = SliderDialog.MyLabel(name, self)
        self._labels.append(label)

        slider = FloatSliderWithEditor()
        slider_changed = self._make_slider_changed(name)
        self._sliders.append(slider)
        connect(slider.valueChanged, slider_changed)

        self._layout.addRow(label, slider)
        self.setLayout(self._layout)

    def get_items(self):
        for label, slider in zip(self._labels, self._sliders):
            pass

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
