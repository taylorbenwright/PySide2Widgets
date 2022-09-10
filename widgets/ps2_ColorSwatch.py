from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Signal


class ColorSwatch(QtWidgets.QPushButton):
    """
    This is a clickable color swatch that can return it's own color.
    """

    def __init__(self, color, *args, **kwargs):
        """
        :param color: A QColor object that describes which color this swatch should be
        :type color: QtGui.QColor object
        """
        super(ColorSwatch, self).__init__(*args, **kwargs)

        self._color = color
        self.setAutoFillBackground(True)
        self.setStyleSheet(self.get_stylesheet_str())

    def get_stylesheet_str(self) -> str:
        red, green, blue = self.color.red(), self.color.green(), self.color.blue()
        return f"QPushButton {{ background-color: rgb({red}, {green}, {blue}); border: 0; }}"

    @property
    def color(self) -> QtGui.QColor:
        return self._color

    @color.setter
    def color(self, value: QtGui.QColor):
        self._color = value
        self.setStyleSheet(self.get_stylesheet_str())
