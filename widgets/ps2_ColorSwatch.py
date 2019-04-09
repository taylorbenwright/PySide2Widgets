from PySide2 import QtWidgets, QtGui


class ColorSwatch(QtWidgets.QPushButton):
    """
    This is a clickable color swatch that can return it's own color.
    """
    def __init__(self, color, color_name, *args, **kwargs):
        """
        :param color: A QColor object that described which color this swatch should be
        :type color: QtGui.QColor object
        """
        super(ColorSwatch, self).__init__(*args, **kwargs)

        self._color = color
        self._color_name = color_name  # type: str
        self.setAutoFillBackground(True)
        self.setStyleSheet('QPushButton { background-color: %s; border: 0; }' % color.name())
        self.setToolTip(self.color_name.lower())

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if type(value) == QtGui.QColor:
            self._color = value
            self.setStyleSheet('QPushButton { background-color: %s; border: 0; }' % self.color.name())

    @property
    def color_name(self):
        return self._color_name
