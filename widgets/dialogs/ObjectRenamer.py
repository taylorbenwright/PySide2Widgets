"""
This tool allows for robust renaming of objects based on wildcards, prefixes, suffixes, numerations, etc.

This tool should only take in a List of strings and return a List of strings
"""

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt, QModelIndex, Signal
import math


class RenameSelectionModel(QtGui.QStandardItemModel):
    def __init__(self, rows, columns, parent=None):
        super(RenameSelectionModel, self).__init__(rows, columns, parent)

        self.parent_item = self.invisibleRootItem()

        self.headers = ['Current Name', 'New Name']

        for ind, col_name in enumerate(self.headers):
            self.setHeaderData(ind, Qt.Horizontal, col_name)

    def add_data(self, selection_data):
        """
        Adds an item into each header of the model with the appropraite data
        :param selection_data: The string of the currently selected item for this index
        :type selection_data: str
        :return: Nothing
        :rtype: None
        """
        current_name_column = QtGui.QStandardItem()
        current_name_column.setData(selection_data, Qt.DisplayRole)
        current_name_column.setEditable(False)

        new_name_column = QtGui.QStandardItem()
        new_name_column.setData('New Name', Qt.DisplayRole)
        new_name_column.setEditable(False)

        self.appendRow([current_name_column, new_name_column])


class ObjectRenamer(QtWidgets.QWidget):

    renamed = Signal(list)
    ready = Signal()

    def __init__(self, *args, **kwargs):
        super(ObjectRenamer, self).__init__(*args, **kwargs)

        self.selected_items = []

        self.generate_ui()

    def dialog_opened(self):
        self.ready.emit()

    def dialog_closed(self):
        pass

    def generate_ui(self):
        main_layout = QtWidgets.QVBoxLayout()

        # Line Edits
        editline_grid = QtWidgets.QGridLayout()
        editline_grid.setColumnStretch(1, 1)
        editline_grid.setAlignment(Qt.AlignTop)

        lineedit_grp = []

        # self.prefix_chx = QtWidgets.QCheckBox()
        self.prefix_chx = QtWidgets.QCheckBox()
        self.prefix_chx.stateChanged.connect(self.checkbox_cycled)
        prefix_label = QtWidgets.QLabel('Prefix:')
        self.prefix_le = QtWidgets.QLineEdit()
        self.prefix_le.setEnabled(False)
        self.prefix_le.textChanged.connect(self.create_new_name)
        lineedit_grp.append((self.prefix_chx, prefix_label, self.prefix_le))

        self.base_name_chx = QtWidgets.QCheckBox()
        self.base_name_chx.stateChanged.connect(self.checkbox_cycled)
        base_name_label = QtWidgets.QLabel('Base Name:')
        self.base_name_le = QtWidgets.QLineEdit()
        self.base_name_le.setEnabled(False)
        self.base_name_le.textChanged.connect(self.create_new_name)
        lineedit_grp.append((self.base_name_chx, base_name_label, self.base_name_le))

        self.side_chx = QtWidgets.QCheckBox()
        self.side_chx.stateChanged.connect(self.checkbox_cycled)
        side_label = QtWidgets.QLabel('Side:')
        self.side_le = QtWidgets.QLineEdit()
        self.side_le.setEnabled(False)
        self.side_le.textChanged.connect(self.create_new_name)
        lineedit_grp.append((self.side_chx, side_label, self.side_le))

        self.suffix_chx = QtWidgets.QCheckBox()
        self.suffix_chx.stateChanged.connect(self.checkbox_cycled)
        suffix_label = QtWidgets.QLabel('Suffix:')
        self.suffix_le = QtWidgets.QLineEdit()
        self.suffix_le.setEnabled(False)
        self.suffix_le.textChanged.connect(self.create_new_name)
        lineedit_grp.append((self.suffix_chx, suffix_label, self.suffix_le))

        self.separator_chx = QtWidgets.QCheckBox()
        self.separator_chx.stateChanged.connect(self.checkbox_cycled)
        separator_label = QtWidgets.QLabel('Separator:')
        self.separator_le = QtWidgets.QLineEdit()
        self.separator_le.setEnabled(False)
        self.separator_le.setText('_')
        self.separator_le.textChanged.connect(self.create_new_name)
        lineedit_grp.append((self.separator_chx, separator_label, self.separator_le))

        self.numeration_chx = QtWidgets.QCheckBox()
        self.numeration_chx.stateChanged.connect(self.checkbox_cycled)
        numeration_label = QtWidgets.QLabel('Numeration:')
        self.numeration_sb = QtWidgets.QSpinBox()
        self.numeration_sb.setEnabled(False)
        self.numeration_sb.setValue(2)
        self.numeration_sb.valueChanged.connect(self.create_new_name)
        lineedit_grp.append((self.numeration_chx, numeration_label, self.numeration_sb))

        num_start_label = QtWidgets.QLabel('Start Number:')
        self.num_start_sb = QtWidgets.QSpinBox()
        self.num_start_sb.setEnabled(False)
        self.num_start_sb.setValue(1)
        self.num_start_sb.valueChanged.connect(self.create_new_name)
        lineedit_grp.append((QtWidgets.QWidget(), num_start_label, self.num_start_sb))

        remove_first_label = QtWidgets.QLabel("Remove First:")
        self.remove_first_sb = QtWidgets.QSpinBox()
        self.remove_first_sb.setValue(0)
        self.remove_first_sb.valueChanged.connect(self.create_new_name)
        lineedit_grp.append((QtWidgets.QWidget(), remove_first_label, self.remove_first_sb))

        remove_last_label = QtWidgets.QLabel("Remove Last:")
        self.remove_last_sb = QtWidgets.QSpinBox()
        self.remove_last_sb.setValue(0)
        self.remove_last_sb.valueChanged.connect(self.create_new_name)
        lineedit_grp.append((QtWidgets.QWidget(), remove_last_label, self.remove_last_sb))

        for ind, (chx, label, le) in enumerate(lineedit_grp):
            editline_grid.addWidget(chx, ind, 0)
            editline_grid.addWidget(label, ind, 1, alignment=Qt.AlignLeft)
            editline_grid.addWidget(le, ind, 2)

        del lineedit_grp

        # Selection Model
        self.list_model = RenameSelectionModel(0, 2, self)

        # Selection Listview
        item_treeview = QtWidgets.QTreeView()
        item_treeview.setModel(self.list_model)

        # Rename Button
        rename_but = QtWidgets.QPushButton('Rename')
        rename_but.clicked.connect(self.do_rename)

        main_layout.addLayout(editline_grid)
        main_layout.addWidget(item_treeview)
        main_layout.addWidget(rename_but)

        self.setLayout(main_layout)

    def clear_selection_list(self):
        """
        Clears out the item model, emptying our list
        :return: Nothing
        :rtype: None
        """
        self.list_model.beginRemoveRows(QModelIndex(), 0, self.list_model.rowCount())

        self.list_model.removeRows(0, self.list_model.rowCount())

        self.list_model.endRemoveRows()

    def selection_changed(self, selection_list):
        """
        The current DCC selection has been changed. Invalidate the current list, empty it, and remake the listview
        :param selection_list: A list containing the short names for all selected objects, in the order they were
                                selected
        :type selection_list: list[str]
        :return: Nothing
        :rtype: None
        """
        self.clear_selection_list()
        self.selected_items = selection_list

        self.list_model.beginInsertRows(QModelIndex(), 0, len(self.selected_items)-1)

        for item in self.selected_items:
            self.list_model.add_data(item)

        self.list_model.endInsertRows()

        self.create_new_name()

    def checkbox_cycled(self, *args):
        sender = self.sender()
        state = bool(args[0])

        lineedit = []
        if sender == self.prefix_chx:
            lineedit.append(self.prefix_le)
        elif sender == self.base_name_chx:
            lineedit.append(self.base_name_le)
        elif sender == self.side_chx:
            lineedit.append(self.side_le)
        elif sender == self.suffix_chx:
            lineedit.append(self.suffix_le)
        elif sender == self.separator_chx:
            lineedit.append(self.separator_le)
        elif sender == self.numeration_chx:
            lineedit.append(self.numeration_sb)
            lineedit.append(self.num_start_sb)

        for le in lineedit:
            le.setEnabled(state)

        self.create_new_name()

    def get_new_names(self):
        """
        Queries the list and gathers all the New Names, returning a list of them
        :return: A list of all the new names
        :rtype: list[str]
        """
        new_names = [None] * self.list_model.rowCount()
        for i in range(self.list_model.rowCount()):
            new_name_index = self.list_model.index(i, 1)
            new_names[i] = self.list_model.data(new_name_index, Qt.DisplayRole)
        return new_names

    def create_new_name(self):
        base_name = self.base_name_le.text() if self.base_name_le.isEnabled() else ''
        prefix = self.prefix_le.text() if self.prefix_le.isEnabled() else ''
        suffix = self.suffix_le.text() if self.suffix_le.isEnabled() else ''
        side = self.side_le.text() if self.side_le.isEnabled() else ''
        separator = self.separator_le.text() if self.separator_le.isEnabled() else ''

        row_digits = int(math.log10(self.list_model.rowCount()))+1 if self.list_model.rowCount() > 0 else 0
        numeration_digits = self.numeration_sb.value() if self.numeration_sb.value() > row_digits else row_digits

        for i in range(self.list_model.rowCount()):
            current_name_index = self.list_model.index(i, 0)
            new_name_index = self.list_model.index(i, 1)
            current_name = self.list_model.data(current_name_index, Qt.DisplayRole)

            new_base_name = base_name if base_name != '' else current_name
            new_prefix = '{}{}'.format(prefix, separator) if prefix != '' else ''
            new_side = '{}{}'.format(separator, side) if side != '' else ''
            new_suffix = '{}{}'.format(separator, suffix) if suffix != '' else ''

            number = str(i+self.num_start_sb.value()).zfill(numeration_digits)
            number = '{}{}'.format(separator, number) if numeration_digits > 0 else number
            number = number if self.numeration_sb.isEnabled() else ''

            final_name = '{}{}{}{}{}'.format(new_prefix, new_base_name, new_side, new_suffix, number)

            final_name = final_name[self.remove_first_sb.value():len(final_name)-self.remove_last_sb.value()]

            self.list_model.setData(new_name_index, final_name, Qt.DisplayRole)

    def do_rename(self):
        """
        This performs the rename operation. It sends the new names to the DCC and then empties the list
        :return: Nothing
        :rtype: None
        """
        self.renamed.emit(self.get_new_names())
        self.clear_selection_list()
        self.ready.emit()
