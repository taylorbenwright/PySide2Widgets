from PySide2 import QtWidgets
from PySide2.QtCore import Signal


class EditableTextBoxLabel(QtWidgets.QWidget):
    """
    Creates a label and an editable text box. The label can be on the left or right
    """

    returnPressed = Signal(str)

    def __init__(self, label_text: str, *args, left_label=True, **kwargs):
        super(EditableTextBoxLabel, self).__init__(*args, **kwargs)

        self.main_layout = QtWidgets.QHBoxLayout()
        label_widget = QtWidgets.QLabel(label_text)
        self.editable_text_widget = QtWidgets.QLineEdit()
        self.editable_text_widget.returnPressed.connect(self.return_pressed)

        if left_label:
            self.main_layout.addWidget(label_widget)
        self.main_layout.addWidget(self.editable_text_widget)
        if not left_label:
            self.main_layout.addWidget(label_widget)

        self.setLayout(self.main_layout)

    @property
    def line_text(self):
        return self.editable_text_widget.text()

    @line_text.setter
    def line_text(self, value: str):
        self.editable_text_widget.setText(value)

    @property
    def layout(self):
        return self.main_layout


    def return_pressed(self, *args):
        self.returnPressed.emit(self.editable_text_widget)
