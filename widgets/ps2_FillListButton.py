from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Signal, QStringListModel


class FillListButton(QtWidgets.QWidget):
    """
    Creates a QListView widget that can be filled with a QPushButton
    """

    clicked = Signal()

    def __init__(self, *args, **kwargs):

        super(FillListButton, self).__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()
        self.list_model = QStringListModel()
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
    def list_text(self, value: list[str]):
        self.list_model.setStringList(value)

    def add_value_to_list(self, value: str):
        str_list = self.list_text
        str_list.append(value)
        self.list_text = str_list

    def on_clicked(self):
        self.clicked.emit()


"""
Demonstrations:

        self.rename_box = ps2_RenameList.RenameList(starting_list=['This', 'Is', 'Rename', 'List'], expandable=True)
        rename_box_items = self.rename_box.items
"""
