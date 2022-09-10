from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import SIGNAL, Signal


class EditableLabel(QtWidgets.QWidget):
    """
    A QLabel which can be edited via left mouse double click, triggering a callback after the text is edited.
    """

    changed = Signal()  # emitted after successful edit

    def __init__(self, *args, **kwargs):
        super(EditableLabel, self).__init__()

        self.label = QtWidgets.QLabel(*args, **kwargs)
        self._lineedit = QtWidgets.QLineEdit()
        self._layout = QtWidgets.QStackedLayout()
        self.generate_ui()

    def generate_ui(self):
        # event handlers
        self.label.mouseDoubleClickEvent = self.on_clicked
        self._lineedit.editingFinished.connect(self.on_edited)

        # layout
        self._layout.addWidget(self.label)
        self._layout.addWidget(self._lineedit)
        self.setLayout(self._layout)
        self._layout.setCurrentIndex(0)

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

    def on_clicked(self, event):
        """Display a QLineEdit to edit the label text"""
        self._layout.setCurrentIndex(1)
        self._lineedit.setText(self.label.text())
        self._lineedit.setFocus()
        self._lineedit.selectAll()

    def on_edited(self):
        """Changes the label text, hides the QLineEdit, and triggers a callback upon successful edit."""
        if self._lineedit.isModified():
            self.label.setText(self._lineedit.text())
            self.emit(SIGNAL('changed()'))
        self._layout.setCurrentIndex(0)
        self._lineedit.clearFocus()
        self._lineedit.blockSignals(False)

    def keyPressEvent(self, event):
        """Watch for the escape key to exit editing mode"""
        if event.key() == QtCore.Qt.Key_Escape:
            self._lineedit.undo()
            self._layout.setCurrentIndex(0)
            self._lineedit.clearFocus()
            self._lineedit.blockSignals(False)
