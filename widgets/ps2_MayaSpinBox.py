from PySide2 import QtWidgets, QtGui, QtCore


class MayaSpinbox(QtWidgets.QDoubleSpinBox):

    def __init__(self, minimum=-99.99, maximum=99.99, start_val=0.00, decimals=2, speed=0.5, *args, **kwargs):
        """
        A spinbox to simulate Maya's native spinbox, allowing drag functionality to change the value.

        :param minimum: The minimum this spinner will go to.
        :type minimum: float|int
        :param maximum: The maximum this spinner will go to.
        :type maximum: float|int
        :param start_val: The default value of this spinner.
        :type start_val: float|int
        :param decimals: How many decimal places the spinner should display.
        :type decimals: int
        :param speed: How fast should this spinner spin with a drag movement? Higher numbers equal a faster spin
        :type speed: float|int
        """

        super(MayaSpinbox, self).__init__(*args, **kwargs)

        self.setAlignment(QtCore.Qt.AlignRight)
        self.setRange(minimum, maximum)
        self.setButtonSymbols(self.NoButtons)
        self.setDecimals(decimals)
        self.setValue(start_val)
        self.lineEdit().installEventFilter(self)
        self._speed = speed

    def get_is_dragging(self):
        """
        Does this widget have mouse focus?

        :return: True if this widget has mouse focus, false otherwise.
        :rtype: bool
        """
        return self.mouseGrabber() == self

    def drag_start(self):
        """
        Begins the drag event, grabbing focus, mouse position in screen space, and setting an initial value to augment.
        :return:
        :rtype:
        """
        self.grabMouse()
        self.drag_origin = QtGui.QCursor().pos()
        self.drag_start_val = self.value()

    def drag_update(self):
        """
        Does the actual drag calculation based on mouse movement and updates current value.
        :return:
        :rtype:
        """
        current_pos = QtGui.QCursor().pos()
        offset_val = (current_pos.x() - self.drag_origin.x()) * self._speed
        new_val = self.drag_start_val + offset_val
        self.setValue(new_val)

    def drag_end(self):
        """
        Ends the drag event, releasing mouse focus and resetting the needed variable.
        """
        self.releaseMouse()
        self.drag_origin = None

    def eventFilter(self, widget, event):
        """
        This eventFilter is needed to give the QLineEdit element of the QDoubleSpinBox the ability to grab key events
        """
        modifiers = QtGui.QGuiApplication.keyboardModifiers()
        if event.type() == QtCore.QEvent.MouseButtonPress and modifiers == QtCore.Qt.ControlModifier and \
                        event.button() == QtCore.Qt.MiddleButton:
            self.drag_start()
            return True
        else:
            return super(MayaSpinbox, self).eventFilter(widget, event)

    def mouseMoveEvent(self, event):
        """
        Continue drag event
        """
        if event.type() == QtCore.QEvent.MouseMove:
            if self.get_is_dragging() and QtCore.Qt.MiddleButton and QtCore.Qt.ControlModifier:
                self.drag_update()
            else:
                super(MayaSpinbox, self).mouseMoveEvent(event)
        else:
            super(MayaSpinbox, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        End drag event.
        """
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if self.get_is_dragging() and QtCore.Qt.MiddleButton:
                self.drag_end()
        else:
            super(MayaSpinbox, self).mouseReleaseEvent(event)

    def keyReleaseEvent(self, event):
        """
        End drag event if the Ctrl key is released prematurely.
        """
        if event.type() == QtCore.QEvent.KeyRelease and QtCore.Qt.ControlModifier and self.get_is_dragging():
            self.drag_end()
        else:
            super(MayaSpinbox, self).keyReleaseEvent(event)


"""
Demonstrations:

        self.spin_box = MayaSpinbox(minimum=-999.0, maximum=999.0, speed=0.05)
        self.spin_box.valueChanged.connect(self.spinbox_changed)
        
        def spinbox_changed(self):
            sender = self.sender()
            if sender.isEnabled():
                value = sender.value()
"""
