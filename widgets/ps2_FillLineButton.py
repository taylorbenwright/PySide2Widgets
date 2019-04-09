from PySide2 import QtWidgets
from PySide2.QtCore import SIGNAL, Signal


class FillLineButton(QtWidgets.QWidget):
    """
    Creates a QLineEdit widget that can be filled with a QPushButton
    """

    clicked = Signal()

    def __init__(self, empty_text='', *args, **kwargs):

        super(FillLineButton, self).__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setPlaceholderText(empty_text)
        self.fill_button = QtWidgets.QPushButton('<<')

        self.generate_ui()

    def generate_ui(self):
        self.fill_button.clicked.connect(self.on_clicked)

        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.fill_button)
        self.setLayout(self.layout)

    @property
    def line_text(self):
        return self.line_edit.text()

    @line_text.setter
    def line_text(self, value):
        self.line_edit.setText(value)

    def on_clicked(self):
        self.emit(SIGNAL('clicked()'))


"""
Demostration:

        self.fill_button = fill_line_button.FillLineButton(empty_text="Fill Button Demo")
        self.fill_button.clicked.connect(self.fill_button_def)
        
        def fill_button_def(self):
            self.fill_button.line_text = "New Line Text"
        
"""
