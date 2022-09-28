from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Signal


class LabelWithCheckbox(QtWidgets.QWidget):
    """
    Creates a label with a checkbox
    """

    value_changed = Signal(bool)

    def __init__(self, label_text: str, starting_val: bool, *args, **kwargs):
        super(LabelWithCheckbox, self).__init__(*args, **kwargs)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
        label_widget = QtWidgets.QLabel(label_text)
        self.value_widget = QtWidgets.QCheckBox()
        self.value_widget.setChecked(starting_val)
        self.value_widget.stateChanged.connect(self.checkbox_value_changed)

        self.main_layout.addWidget(label_widget)
        self.main_layout.addWidget(self.value_widget)

        self.setLayout(self.main_layout)

    @property
    def layout(self):
        return self.main_layout

    @property
    def value(self):
        return self.value_widget.isChecked()

    @value.setter
    def value(self, value: bool):
        self.value_widget.setChecked(value)

    def checkbox_value_changed(self, *args):
        self.value_changed.emit(self.value_widget.isChecked())
