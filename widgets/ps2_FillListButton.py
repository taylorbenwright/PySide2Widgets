from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import SIGNAL, Signal


class FillListButton(QtWidgets.QWidget):
    """
    Creates a QListView widget that can be filled with a QPushButton
    """

    clicked = Signal()

    def __init__(self, *args, **kwargs):

        super(FillListButton, self).__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()
        self.list_model = QtGui.QStringListModel()
        self.list = QtWidgets.QListView()

        self.list.setModel(self.list_model)
        self.fill_button = QtWidgets.QPushButton('<<')

        self.generate_ui()

    def generate_ui(self):
        self.fill_button.clicked.connect(self.on_clicked)

        self.layout.addWidget(self.list)
        self.layout.addWidget(self.fill_button)
        self.setLayout(self.layout)

    @property
    def list_text(self):
        return self.list_model.stringList()

    @list_text.setter
    def list_text(self, value):
        if isinstance(value, list):
            self.list_model.setStringList(value)

    def on_clicked(self):
        self.emit(SIGNAL('clicked()'))


"""
Demostration:

        self.fill_button = fill_list_button.FillListButton()
        self.fill_button.clicked.connect(self.fill_button_def)
        
        def fill_button_def(self):
            self.fill_button.list_text = ['01', '02', '03']
        
"""
