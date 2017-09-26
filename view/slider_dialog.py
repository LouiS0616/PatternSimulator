from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout
from PyQt5.QtGui import QFont

from FloatSlider.slider import FloatSliderWithEditor


class SliderDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, parent=None)
        self._layout = QFormLayout()

    def add_row(self, name: str) -> None:
        label = self.MyLabel(name, self)
        self._layout.addRow(
            label, FloatSliderWithEditor()
        )
        self.setLayout(self._layout)

    class MyLabel(QLabel):
        font = QFont('consolas')

        def __init__(self, text: str, parent):
            QLabel.__init__(self, text=text, parent=parent)
            self.setFont(self.font)
            self.setAlignment(Qt.AlignBottom)
