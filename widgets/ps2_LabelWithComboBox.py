from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Signal


class LabelWithComboBox(QtWidgets.QWidget):
    """
    Creates a label with a combobox to the left of it
    """

    index_changed = Signal(int, str)

    def __init__(self, label_text: str, combo_list: list, *args, **kwargs):
        super(LabelWithComboBox, self).__init__(*args, **kwargs)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
        label_widget = QtWidgets.QLabel(label_text)
        self.combo_widget = QtWidgets.QComboBox()
        self.combo_widget.insertItems(0, combo_list)
        self.combo_widget.currentIndexChanged.connect(self.combobox_index_changed)

        self.main_layout.addWidget(label_widget)
        self.main_layout.addWidget(self.combo_widget)

        self.setLayout(self.main_layout)

    @property
    def layout(self):
        return self.main_layout

    @property
    def index(self):
        return self.combo_widget.currentIndex()

    @index.setter
    def index(self, value: int):
        self.combo_widget.setCurrentIndex(value)

    def combobox_index_changed(self, *args):
        ind = args[0]
        val = self.combo_widget.itemText(ind)
        self.index_changed.emit(ind, val)
