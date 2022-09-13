"""
This tools spits out a dict in the form:

thing = {'set_name': {'path': 'c:/path/to/export',
                      'origin': int
                      'zero_out': int,
                      'smoothing_groups': int,
                      'triangulate': int,
                      'turbosmooth': int,
                      'tanbi': int,
                      'svn': int,
                      'skinning': int,
                      'sceneup': int,
                      }
         }

This is written and read from the scene. In Max, it is in a json dict on the rootnode. In Maya, it is held in a network
node. Either way the input to the tool is a dict with the same format as above.

"""

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt, Signal, QModelIndex
from os.path import abspath
from gui.ps2_BoxLayoutSeparator import BoxLayoutSeparator
from gui.ps2_TristateCheckbox import TristateCheckbox


SELECTION_SET_OPERATIONS = ['created', 'deleted', 'name_changed']

# These are based on the Qt::Role int values. UserRole starts at 32
SETTINGS__ = {'name': 0,
              'path': 32,
              'origin': 33,
              'smoothing_groups': 34,
              'triangulate': 35,
              'turbosmooth': 36,
              'tanbi': 37,
              'svn': 38,
              'skinning': 39,
              'sceneup': 40}


class ObjectExporter(QtWidgets.QWidget):

    selection_set_changed_signal = Signal(list)
    export_sets_signal = Signal(list)
    ready = Signal()

    def __init__(self, *args, **kwargs):
        self.starting_directory = kwargs.pop('starting_directory', None)
        super(ObjectExporter, self).__init__(*args, **kwargs)

        self.setting_widgets = []
        self.selection_set_items = []  # type: list[QtGui.QStandardItem]

        self.generate_ui()

    def dialog_opened(self):
        self.ready.emit()

    def dialog_closed(self):
        pass

    def generate_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.selection_set_layout = QtWidgets.QVBoxLayout()
        self.selection_set_layout.setAlignment(Qt.AlignTop)

        self.selection_set_model = QtGui.QStandardItemModel()
        self.selection_set_model.appendRow(self.selection_set_items)
        self.selection_set_model.itemChanged.connect(self.selection_set_changed)

        self.selection_set_label = QtWidgets.QLabel('Selection Sets:')
        self.selection_set_listview = QtWidgets.QListView()
        self.selection_set_listview.setFlow(QtWidgets.QListView.TopToBottom)
        self.selection_set_listview.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.selection_set_listview.setModel(self.selection_set_model)
        self.selection_set_listview.selectionModel().selectionChanged.connect(self.selection_set_clicked)
        self.selection_set_listview.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        self.path_line = QtWidgets.QHBoxLayout()
        self.selection_set_path = QtWidgets.QLineEdit()
        self.selection_set_path.setPlaceholderText('Selection Set Export Path...')
        self.selection_set_path.editingFinished.connect(self.selection_set_path_changed)
        self.browse_button = QtWidgets.QPushButton('...')
        self.browse_button.clicked.connect(self.browse_button_clicked)
        self.browse_button.setFixedWidth(30)
        self.path_line.addWidget(self.selection_set_path)
        self.path_line.addWidget(self.browse_button)

        self.selection_set_layout.addWidget(self.selection_set_label)
        self.selection_set_layout.addWidget(self.selection_set_listview)
        self.selection_set_layout.addLayout(self.path_line)

        # Settings
        settings_widget_layout = QtWidgets.QVBoxLayout()
        settings_label = QtWidgets.QLabel('Export Settings:')

        # Geometry
        self.specific_settings_frame = QtWidgets.QVBoxLayout()

        geometry_button_grp = QtWidgets.QGroupBox('Geometry')
        vertical_layout = QtWidgets.QVBoxLayout()
        top_geo_layout = QtWidgets.QGridLayout()
        bot_geo_layout = QtWidgets.QGridLayout()

        self.smoothing_group_chx = TristateCheckbox('Smoothing Groups')
        self.smoothing_group_chx.setObjectName('smoothing_groups')
        self.turbosmooth_chx = TristateCheckbox('TurboSmooth')
        self.turbosmooth_chx.setObjectName('turbosmooth')
        self.split_vertex_normals_chx = TristateCheckbox('Split-Vertex Normals')
        self.split_vertex_normals_chx.setObjectName('svn')
        self.triangulate_chx = TristateCheckbox('Triangulate')
        self.triangulate_chx.setObjectName('triangulate')
        self.tangents_binormals_chx = TristateCheckbox('Tangents && Binormals')
        self.tangents_binormals_chx.setObjectName('tanbi')
        self.skinning_chx = TristateCheckbox('Skinning')
        self.skinning_chx.setObjectName('skinning')
        self.up_axis_cbx = QtWidgets.QComboBox()
        self.up_axis_cbx.addItems(['Y', 'Z'])
        self.up_axis_cbx.setObjectName('sceneup')

        self.smoothing_group_chx.setEnabled(False)
        self.turbosmooth_chx.setEnabled(False)
        self.split_vertex_normals_chx.setEnabled(False)
        self.triangulate_chx.setEnabled(False)
        self.tangents_binormals_chx.setEnabled(False)
        self.skinning_chx.setEnabled(False)
        self.up_axis_cbx.setEnabled(False)

        self.setting_widgets.append(self.smoothing_group_chx)
        self.setting_widgets.append(self.turbosmooth_chx)
        self.setting_widgets.append(self.split_vertex_normals_chx)
        self.setting_widgets.append(self.triangulate_chx)
        self.setting_widgets.append(self.tangents_binormals_chx)
        self.setting_widgets.append(self.skinning_chx)
        self.setting_widgets.append(self.up_axis_cbx)

        top_geo_layout.addWidget(self.smoothing_group_chx, 0, 0)
        top_geo_layout.addWidget(self.turbosmooth_chx, 1, 0)
        top_geo_layout.addWidget(self.split_vertex_normals_chx, 2, 0)
        top_geo_layout.addWidget(self.triangulate_chx, 0, 1)
        top_geo_layout.addWidget(self.tangents_binormals_chx, 1, 1)

        bot_geo_layout.addWidget(self.skinning_chx, 0, 0)
        bot_geo_layout.addWidget(self.up_axis_cbx, 0, 1)

        vertical_layout.addLayout(top_geo_layout)
        vertical_layout.addWidget(BoxLayoutSeparator(QtWidgets.QFrame.HLine))
        vertical_layout.addLayout(bot_geo_layout)
        geometry_button_grp.setLayout(vertical_layout)

        self.specific_settings_frame.addWidget(geometry_button_grp)

        general_settings_frame = QtWidgets.QVBoxLayout()
        general_settings_groupbox = QtWidgets.QGroupBox('General Settings')
        general_settings_grid = QtWidgets.QGridLayout()

        self.zero_out_chx = TristateCheckbox('Zero Out')
        self.zero_out_chx.setObjectName('origin')
        self.zero_out_chx.setEnabled(False)
        self.setting_widgets.append(self.zero_out_chx)

        for widget in self.setting_widgets:
            if isinstance(widget, QtWidgets.QCheckBox):
                widget.setTristate(True)
                widget.stateChanged.connect(self.setting_changed)
            elif isinstance(widget, QtWidgets.QComboBox):
                widget.currentIndexChanged.connect(self.setting_changed)

        general_settings_grid.addWidget(self.zero_out_chx, 0, 0)
        general_settings_groupbox.setLayout(general_settings_grid)
        general_settings_frame.addWidget(general_settings_groupbox)

        settings_widget_layout.addWidget(settings_label)
        settings_widget_layout.addLayout(self.specific_settings_frame)
        settings_widget_layout.addLayout(general_settings_frame)

        # Export
        self.export_but = QtWidgets.QPushButton('Export Selected')
        self.export_but.setEnabled(False)
        self.export_but.clicked.connect(self.export_but_clicked)

        # Main Widget
        main_layout.addLayout(self.selection_set_layout)
        main_layout.addWidget(BoxLayoutSeparator(QtWidgets.QFrame.HLine))
        main_layout.addLayout(settings_widget_layout)
        main_layout.addWidget(self.export_but)

        self.setLayout(main_layout)

    @staticmethod
    def scene_data_to_standard_items(scene_data):
        """
        Takes in the json data from the scene and translates it into QStandardItems for consumption
        :param scene_data: A list of set dictionaries
        :type scene_data: list
        :return: A list of QStandardItems
        :rtype: list
        """
        standard_items = []
        for item in scene_data:  # type: dict
            if not hasattr(item, 'get'):
                continue
            new_item = QtGui.QStandardItem(item.get('name', None))
            new_item.setEditable(False)

            path = abspath(item['path']) if 'path' in item else None
            new_item.setData(path, role=SETTINGS__['path'])

            new_item.setData(item.get('smoothing_groups', 0), role=SETTINGS__['smoothing_groups'])
            new_item.setData(item.get('triangulate', 0), role=SETTINGS__['triangulate'])
            new_item.setData(item.get('turbosmooth', 0), role=SETTINGS__['turbosmooth'])
            new_item.setData(item.get('tanbi', 0), role=SETTINGS__['tanbi'])
            new_item.setData(item.get('svn', 0), role=SETTINGS__['svn'])
            new_item.setData(item.get('skinning', 0), role=SETTINGS__['skinning'])
            new_item.setData(item.get('sceneup', 0), role=SETTINGS__['sceneup'])
            new_item.setData(item.get('origin', 0), role=SETTINGS__['origin'])

            standard_items.append(new_item)
        return standard_items

    @staticmethod
    def standard_item_to_scene_data(standard_item):
        """
        Takes in a QStandardItem and creates an export dict from the Items various UserRoles
        :param standard_item: The QStandardItem we want to translate
        :type standard_item: QtGui.QStandardItem
        :return: The translated dictionary with all the payload data
        :rtype: dict
        """
        scene_data = dict()
        scene_data['name'] = standard_item.data(role=Qt.DisplayRole)
        scene_data['path'] = standard_item.data(role=SETTINGS__['path'])
        scene_data['smoothing_groups'] = standard_item.data(role=SETTINGS__['smoothing_groups'])
        scene_data['triangulate'] = standard_item.data(role=SETTINGS__['triangulate'])
        scene_data['turbosmooth'] = standard_item.data(role=SETTINGS__['turbosmooth'])
        scene_data['tanbi'] = standard_item.data(role=SETTINGS__['tanbi'])
        scene_data['svn'] = standard_item.data(role=SETTINGS__['svn'])
        scene_data['skinning'] = standard_item.data(role=SETTINGS__['skinning'])
        scene_data['sceneup'] = standard_item.data(role=SETTINGS__['sceneup'])
        scene_data['origin'] = standard_item.data(role=SETTINGS__['origin'])
        return scene_data

    @staticmethod
    def create_default_selection_set(set_name):
        """
        Creates a StandardItem with the given name and all default values. Adds this to the end of the list, then
        :param set_name: The name we want the new set to have
        :type set_name: str
        :return: The resultant QStandardItem
        :rtype: QtGui.QStandardItem
        """
        new_item = QtGui.QStandardItem(set_name)
        new_item.setEditable(False)

        new_item.setData('', role=SETTINGS__['path'])

        new_item.setData(0, role=SETTINGS__['smoothing_groups'])
        new_item.setData(0, role=SETTINGS__['triangulate'])
        new_item.setData(0, role=SETTINGS__['turbosmooth'])
        new_item.setData(0, role=SETTINGS__['tanbi'])
        new_item.setData(0, role=SETTINGS__['svn'])
        new_item.setData(0, role=SETTINGS__['skinning'])
        new_item.setData(0, role=SETTINGS__['sceneup'])
        new_item.setData(0, role=SETTINGS__['origin'])

        return new_item

    def get_named_selection_set(self, set_name):
        """
        Gets a selection set based on its name
        :param set_name: The name of the selection set to grab
        :type set_name: str
        :return: The selection set we have found or None
        :rtype: QtGui.QStandardItem | None
        """
        for sel_set in self.selection_set_items:
            if sel_set.data(role=Qt.DisplayRole) == set_name:
                return sel_set
        return None

    def export_but_clicked(self, *args):
        """
        This sends the selected selection sets to the DCC to perform its export procedures.
        :return: Nothing
        :rtype: None
        """
        selected_indexes = self.selection_set_listview.selectionModel().selectedIndexes()
        selected_sets = [self.selection_set_model.data(ind, role=Qt.DisplayRole) for ind in selected_indexes]
        self.export_sets_signal.emit(selected_sets)

    def browse_button_clicked(self, *args):
        browser = QtWidgets.QFileDialog(parent=self, caption='Browse for Export Path...', directory=self.starting_directory)
        browser.setFileMode(QtWidgets.QFileDialog.Directory)
        browser.setOptions(QtWidgets.QFileDialog.ShowDirsOnly)
        self.selection_set_path.setText((browser.getExistingDirectory()).replace('/', '\\'))
        self.selection_set_path.editingFinished.emit()

    def selection_set_clicked(self, *args):
        """
        Callback for when the current selection in the list is changed
        :return: Nothing
        :rtype: None
        """
        selected_indexes = self.selection_set_listview.selectionModel().selectedIndexes()
        if len(selected_indexes) == 0:
            self.export_but.setEnabled(False)

            self.selection_set_path.blockSignals(True)
            self.selection_set_path.setText('')
            self.selection_set_path.blockSignals(False)

            for widget in self.setting_widgets:
                widget.blockSignals(True)
                widget.setEnabled(False)
                widget.blockSignals(True)

        elif len(selected_indexes) == 1:
            ind = selected_indexes[0]
            self.export_but.setEnabled(True)

            self.selection_set_path.blockSignals(True)
            self.selection_set_path.setText(self.selection_set_model.data(ind, role=SETTINGS__['path']))
            self.selection_set_path.blockSignals(False)

            for widget in self.setting_widgets:  # type: QtWidgets.QWidget
                widget.blockSignals(True)
                widget.setEnabled(True)

                name = widget.objectName()
                if isinstance(widget, TristateCheckbox):
                    state_int = self.selection_set_model.data(ind, role=SETTINGS__[name])
                    state = Qt.Unchecked if state_int == 0 else Qt.Checked
                    widget.setCheckState(state)
                elif isinstance(widget, QtWidgets.QComboBox):
                    widget.setCurrentIndex(self.selection_set_model.data(ind, role=SETTINGS__[name]))

                widget.blockSignals(False)

        elif len(selected_indexes) > 1:
            self.export_but.setEnabled(True)

            self.selection_set_path.blockSignals(True)
            paths = [self.selection_set_model.data(ind, role=SETTINGS__['path']) for ind in selected_indexes]
            if all(path == paths[0] for path in paths):
                self.selection_set_path.setText(paths[0])
            else:
                self.selection_set_path.setText('Multiple Paths')
            self.selection_set_path.blockSignals(False)

            for widget in self.setting_widgets:
                widget.blockSignals(True)
                widget.setEnabled(True)

                name = widget.objectName()

                if isinstance(widget, TristateCheckbox):
                    states_ints = [self.selection_set_model.data(ind, role=SETTINGS__[name]) for ind in selected_indexes]
                    states = [Qt.Unchecked if state_int == 0 else Qt.Checked for state_int in states_ints]

                    if all(state == states[0] for state in states):
                        widget.setCheckState(states[0])
                    else:
                        widget.setCheckState(Qt.PartiallyChecked)

                widget.blockSignals(False)

    def scene_data_changed(self, set_data):
        """
        Used by the calling, DCC dialog to push new selection set data to this dialog
        :param set_data: a list of dicts
        :type set_data: list
        :return: Nothing
        :rtype: None
        """
        self.selection_set_items = self.scene_data_to_standard_items(set_data)
        self.selection_set_model.clear()
        for item in self.selection_set_items:
            self.selection_set_model.appendRow(item)

    def selection_set_changed(self, *args):
        """
        Callback that happens when the dialog updates some data on the QStandardItem. Then we emit the payload back to
        the DCC
        :param args: The QStandardItem that has been changed
        :type args: QtGui.QStandardItem
        :return: Nothing
        :rtype: None
        """
        scene_dicts = [self.standard_item_to_scene_data(item) for item in self.selection_set_items]
        self.selection_set_changed_signal.emit(scene_dicts)

    def setting_changed(self, *args):
        """
        Callback for when a setting is changed on the dialog by the user
        :return: Nothing
        :rtype: None
        """
        for ind in self.selection_set_listview.selectedIndexes():
            self.selection_set_model.setData(ind, args[0], role=SETTINGS__[self.sender().objectName()])

    def selection_set_path_changed(self, *args):
        """
        Callback for when the export path is changed on the dialog by the user
        :return:
        :rtype:
        """
        for ind in self.selection_set_listview.selectedIndexes():
            self.selection_set_model.setData(ind, self.selection_set_path.text(), role=SETTINGS__['path'])

    def create_selection_set(self, set_name):
        """
        Creates a new selection set for this dialog to display
        :param set_name: The name to create the set under
        :type set_name: str
        :return: Nothing
        :rtype: None
        """
        new_item = self.create_default_selection_set(set_name)
        self.selection_set_items.append(new_item)
        self.selection_set_model.clear()
        self.selection_set_model.appendColumn(self.selection_set_items)

    def remove_selection_set(self, set_name):
        """
        Removes a selection set from this dialog
        :param set_name: The set name to remove
        :type set_name: str
        :return: Nothing
        :rtype: None
        """
        index = 0
        for ind, item in enumerate(self.selection_set_items):
            if item.data(role=Qt.DisplayRole) == set_name:
                index = ind
                break

        sel_set = self.selection_set_items.pop(index)
        del sel_set

        self.selection_set_model.clear()
        self.selection_set_model.appendColumn(self.selection_set_items)

    def rename_selection_set(self, set_name, new_name):
        """
        Renames a selection set in the dialog and refreshes the view
        :param set_name: The name of the set being renamed
        :type set_name: str
        :param new_name: The new name to set for the set
        :type new_name: str
        :return: Nothing
        :rtype: None
        """
        sel_set = self.get_named_selection_set(set_name)
        if sel_set is None:
            return
        sel_set.setData(new_name, role=Qt.DisplayRole)

