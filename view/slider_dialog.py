from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QWidget
from PyQt5.QtGui import QFont

from FloatSlider.slider import FloatSliderWithEditor
from MyPyUtil.my_util.qt_util import connect


class SliderDialog(QDialog):
    item_changed = pyqtSignal(str, float)

    def __init__(self):
        QDialog.__init__(self, parent=None)
        self.setWindowFlags(Qt.WindowTitleHint)
        self.setWindowTitle('Param Slider Dialog')
        self._layout = QFormLayout()
        self._labels = []
        self._sliders = []

    def add_row(self, name: str, slider_with_editor: FloatSliderWithEditor=None) -> None:
        label = SliderDialog.MyLabel(name, self)
        self._labels.append(label)

        if slider_with_editor is None:
            slider_with_editor = FloatSliderWithEditor()

        self._sliders.append(slider_with_editor)
        connect(
            slider_with_editor.valueChanged,
            self._make_slider_changed(name)
        )

        self._layout.addRow(label, slider_with_editor)
        self.setLayout(self._layout)

    def get_items(self):
        for label, slider_with_editor in zip(self._labels, self._sliders):
            yield label.text(), slider_with_editor.slider.value()

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
