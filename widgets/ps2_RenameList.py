from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Signal, Slot, Qt


class RenameList(QtWidgets.QWidget):
    def __init__(self, starting_list=None, expandable=False, *args, **kwargs):
        """
        Creates a list box with text entries that can be renamed via a line edit widget. Can be an expanding or static
        list length
        :param starting_list: The strings to begin the list with
        :type starting_list: list[str]
        :param expandable: Is this list expandable when a new entry is added?
        :type expandable: bool
        """
        super(RenameList, self).__init__(*args, **kwargs)

        self.starting_list = starting_list if type(starting_list) == list else []
        self.expandable = expandable

        if expandable:
            self.starting_list.append('')

        main_layout = QtWidgets.QVBoxLayout()

        self.list_box = QtWidgets.QListWidget()
        self.list_box.addItems(self.starting_list)
        self.list_box.currentRowChanged.connect(self.list_index_changed)
        if self.expandable:
            self.list_box.itemChanged.connect(self.item_changed)
        self.rename_view = QtWidgets.QLineEdit()
        self.rename_view.editingFinished.connect(self.rename_editing_finished)

        main_layout.addWidget(self.list_box)
        main_layout.addWidget(self.rename_view)

        self.setLayout(main_layout)

    @property
    def items(self):
        return self.list_box.items()

    def list_index_changed(self, new_index):
        try:
            self.rename_view.setText(self.list_box.item(new_index).data(Qt.DisplayRole))
        except AttributeError:
            pass

    def rename_editing_finished(self):
        if not self.expandable and self.rename_view.text() == '':
            return
        try:
            self.list_box.currentItem().setData(Qt.DisplayRole, self.rename_view.text())
        except AttributeError:
            pass

    def item_changed(self, new_item):
        items_to_remove = []
        for ind, item in enumerate(range(self.list_box.count())):
            if self.list_box.item(ind).data(Qt.DisplayRole) == '':
                items_to_remove.append(ind)
        for ind in reversed(items_to_remove):
            self.list_box.takeItem(ind)

        self.list_box.addItem('')


"""
Demonstrations:

        self.rename_box = ps2_RenameList.RenameList(starting_list=['This', 'Is', 'Rename', 'List'], expandable=True)
        rename_box_items = self.rename_box.items
"""
