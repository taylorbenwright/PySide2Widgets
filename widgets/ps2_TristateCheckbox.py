from PySide2 import QtWidgets
from PySide2.QtCore import Qt


class TristateCheckbox(QtWidgets.QCheckBox):
    """
    A QCheckBox that is TriState enabled, but disallows the user from cycling to the PartiallyChecked state
    """

    def __init__(self, *args, **kwargs):
        super(TristateCheckbox, self).__init__(*args, **kwargs)

        self.setTristate(True)

    def nextCheckState(self):
        match self.checkState():
            case Qt.Unchecked:
                self.setCheckState(Qt.Checked)
            case Qt.PartiallyChecked:
                self.setCheckState(Qt.Checked)
            case Qt.Checked:
                self.setCheckState(Qt.Unchecked)
