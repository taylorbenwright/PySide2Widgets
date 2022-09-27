from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Signal


class LabelWithSpinbox(QtWidgets.QWidget):
    """
    Creates a label with a spinbox widget to the right of it
    """

    value_changed = Signal(float)

    def __init__(self, label_text: str, starting_val: float, *args, **kwargs):
        super(LabelWithSpinbox, self).__init__(*args, **kwargs)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
        label_widget = QtWidgets.QLabel(label_text)
        self.value_widget = QtWidgets.QDoubleSpinBox()
        self.value_widget.setValue(starting_val)
        self.value_widget.valueChanged.connect(self.spinbox_value_changed)

        self.main_layout.addWidget(label_widget)
        self.main_layout.addWidget(self.value_widget)

        self.setLayout(self.main_layout)

    @property
    def layout(self):
        return self.main_layout

    @property
    def value(self):
        return self.value_widget.text()

    @value.setter
    def value(self, value: float):
        self.value_widget.setValue(value)

    def spinbox_value_changed(self, *args):
        self.value_changed.emit(self.value_widget.value())
