from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import SIGNAL, Signal


def clear_layout(layout):
    """
    Removes and deletes all child items of a given layout

    :param layout: The layout to clear
    :type layout: QtWidgets.QLayout

    :return: Nothing
    :rtype: None
    """
    if layout is not None:
        if isinstance(layout, QtWidgets.QLayout):
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    clear_layout(child.layout())
        else:
            raise TypeError('Requested layout must be based from QLayout. Got: {}'.format(type(layout)))


class Rollout(QtWidgets.QWidget):
    """A collapsible container to collapse/expand widget"""
    # _________________________________
    # |                               |
    # |  ...........................  |
    # |  : [>] Label               :  |
    # |  :                         :  |
    # |  :    [WRAPPED_WIDGET]     :  |
    # |  :                         :  |
    # |  :.........................:  |
    # |                               |
    # |_______________________________|

    toggled = Signal()  # emitted after widget toggled
    expanded = Signal()  # emitted after widget expanded
    collapsed = Signal()  # emitted after widget collapsed

    def __init__(self, label=None, border=False, content=None, *args, **kwargs):
        super(Rollout, self).__init__()

        # structure
        main_layout = QtWidgets.QGridLayout()

        self.frame = QtWidgets.QFrame()
        frame_layout = QtWidgets.QVBoxLayout()
        self.frame.setLayout(frame_layout)

        self._title = QtWidgets.QWidget()
        title_layout = QtWidgets.QHBoxLayout()
        self._title.setLayout(title_layout)
        self.button = QtWidgets.QToolButton()

        self._label = QtWidgets.QWidget()
        label_layout = QtWidgets.QHBoxLayout()
        self._label.setLayout(label_layout)
        self.label = label

        title_layout.addWidget(self.button)
        title_layout.addWidget(self._label)

        self._content = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout()
        self._content.setLayout(content_layout)
        self.content = content

        frame_layout.addWidget(self._title)
        frame_layout.addWidget(self._content)
        main_layout.addWidget(self.frame)
        self.setLayout(main_layout)

        # style
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(QtCore.Qt.AlignTop)

        if border:
            self.frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
            self.frame.setLineWidth(1)

        self._title.setAutoFillBackground(True)

        title_layout.setSpacing(0)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setAlignment(QtCore.Qt.AlignLeft)

        label_layout.setSpacing(0)
        label_layout.setContentsMargins(0, 0, 0, 0)

        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        frame_layout.setSpacing(0)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.button.setArrowType(QtCore.Qt.DownArrow)
        self.button.setAutoFillBackground(True)
        self.button.setStyleSheet('QToolButton {'
                                  '     border: none;'
                                  '     qproperty-iconSize: 8px;'
                                  '     padding: 4px;'
                                  '}')
        self.button.clicked.connect(self.toggle)

    @property
    def label(self):
        return [self._label.layout().itemAt(i) for i in range(self._label.layout().count())]

    @label.setter
    def label(self, value):
        """Replaces the label ui with a new QWidget or QLayout"""

        clear_layout(self._label.layout())

        if value:
            if isinstance(value, str):
                default_label = QtWidgets.QLabel(value)
                default_font = QtGui.QFont()
                default_font.setBold(True)
                default_label.setFont(default_font)
                default_label.setContentsMargins(0, 2, 0, 0)
                default_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                default_label.setAutoFillBackground(True)
                self._label.layout().addWidget(default_label)
            elif isinstance(value, QtWidgets.QWidget):
                self._label.layout().addWidget(value)
            elif isinstance(value, QtWidgets.QLayout):
                self._label.layout().addLayout(value)
            else:
                raise TypeError('label must inherit from type QWidget or QLayout')

    @property
    def content(self):
        return [self._content.layout().itemAt(i) for i in range(self._content.layout().count())]

    @content.setter
    def content(self, value):
        """Replaces the content ui with a new QWidget or QLayout"""

        clear_layout(self._content.layout())

        if value:
            if isinstance(value, QtWidgets.QWidget):
                self._content.layout().addWidget(value)
            elif isinstance(value, QtWidgets.QLayout):
                self._content.layout().addLayout(value)
            else:
                raise TypeError('content must inherit from type QWidget or QLayout')

    def is_collapsed(self):
        """Returns the collapsed state of the Rollout"""
        return True if self.button.arrowType() == QtCore.Qt.RightArrow else False

    def is_expanded(self):
        """Returns the expanded state of the Rollout"""
        return True if self.button.arrowType() == QtCore.Qt.DownArrow else False

    def collapse(self):
        """Collapses the state of the Rollout emitting 'collapsed' if successful"""
        if self.is_expanded():
            self._content.setVisible(False)
            self.button.setArrowType(QtCore.Qt.RightArrow)
            self.emit(SIGNAL('collapsed()'))
            return True
        return False

    def expand(self):
        """Expands the state of the Rollout emitting 'expanded' if successful"""
        if self.is_collapsed():
            self._content.setVisible(True)
            self.button.setArrowType(QtCore.Qt.DownArrow)
            self.emit(SIGNAL('expanded()'))
            return True
        return False

    def toggle(self):
        """Toggles the expand/collapse state of the Rollout emitting 'toggled' if successful"""
        if self.is_collapsed():
            toggled = self.expand()
        else:
            toggled = self.collapse()

        if toggled:
            self.emit(SIGNAL('toggled()'))