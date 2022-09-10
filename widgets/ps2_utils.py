from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import SIGNAL, Signal


def clear_layout(layout_object):
    """
    Clears all children from a layout object
    :param layout_object: The layout object to clear
    :type layout_object: QtWidgets.QLayout
    :return: Nothing
    :rtype: None
    """
    child = layout_object.takeAt(0)
    while child:
        try:
            child.widget().setParent(None)
        except AttributeError:
            pass
        del child
        child = layout_object.takeAt(0)
