from PySide2 import QtWidgets, QtCore


class LabelWithValue(QtWidgets.QWidget):
    """
    Creates a label with a value label next to it with an optional stylesheet on the value
    """


    def __init__(self, label_text: str, value_text: str, *args, value_stylesheet: str = '', **kwargs):
        super(LabelWithValue, self).__init__(*args, **kwargs)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
        label_widget = QtWidgets.QLabel(label_text)
        self.value_widget = QtWidgets.QLabel(value_text)
        if value_stylesheet:
            self.value_widget.setStyleSheet(value_stylesheet)

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
    def value(self, value: str):
        self.value_widget.setText(value)
