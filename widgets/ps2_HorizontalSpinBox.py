from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Signal, Slot, Qt


class HorizontalSpinBox(QtWidgets.QHBoxLayout):

    changed = Signal(float)

    def __init__(self, minimum=-99.99, maximum=99.99, start_val=0.00, decimals=2, step=1.0,
                 right_utility=None, left_utility=None,
                 *args, **kwargs):
        """
        Creates a Spinbox with a horizontal layout. Allows for two utility buttons
        :param minimum: The minimum this spinner will go to.
        :type minimum: float
        :param maximum: The maximum this spinner will go to.
        :type maximum: float
        :param start_val: The default value of this spinner.
        :type start_val: float
        :param decimals: How many decimal places the spinner should display.
        :type decimals: int
        :param step: The value we should step by when going up/down
        :type step: float
        :param right_utility: Should there be a right utility button? If so, what should the function be?
        :type right_utility: dict
        :param left_utility: Should there be a left utility button? If so, what should the function be?
        :type left_utility: dict
        """
        super(HorizontalSpinBox, self).__init__(*args, **kwargs)

        self.spinbox = QtWidgets.QDoubleSpinBox()
        self.spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinbox.setRange(minimum, maximum)
        self.spinbox.setValue(start_val)
        self.spinbox.setDecimals(decimals)
        self.spinbox.setSingleStep(step)
        self.spinbox.valueChanged.connect(self.changed)
        self.spinbox.setAlignment(Qt.AlignRight)

        self.plus_but = QtWidgets.QPushButton('>')
        self.plus_but.clicked.connect(self.plus_value)
        self.minus_but = QtWidgets.QPushButton('<')
        self.minus_but.clicked.connect(self.minus_value)

        if left_utility is not None:
            self.left_utility = QtWidgets.QPushButton(left_utility.get('label', ''))
            self.left_utility.clicked.connect(left_utility.get('function', None))
            self.left_utility.setFixedSize(self.left_utility.minimumSizeHint())
            self.addWidget(self.left_utility)

        self.addWidget(self.minus_but)
        self.addWidget(self.spinbox)
        self.addWidget(self.plus_but)

        if right_utility is not None:
            self.right_utility = QtWidgets.QPushButton(right_utility.get('label', ''))
            self.right_utility.clicked.connect(right_utility.get('function', None))
            self.right_utility.setFixedSize(self.right_utility.minimumSizeHint())
            self.addWidget(self.right_utility)

        self.setSpacing(1)

    @property
    def spinbox_value(self):
        return self.spinbox.value()

    @spinbox_value.setter
    def spinbox_value(self, value):
        self.spinbox.setValue(value)

    @property
    def left_utility_button(self):
        return self.left_utility

    @property
    def right_utility_button(self):
        return self.right_utility

    def plus_value(self):
        self.spinbox.setValue(self.spinbox.value() + self.spinbox.singleStep())

    def minus_value(self):
        self.spinbox.setValue(self.spinbox.value() - self.spinbox.singleStep())


"""
Demonstrations:

        right_utility_button = {}
        right_utility_button['label'] = '>>'
        right_utility_button['function'] = self.right_function
        
        left_utility_button = {}
        left_utility_button['label'] = '<<'
        left_utility_button['function'] = self.left_function
        
        self.horizontal_spinbox = ps2_HorizontalSpinBox.HorizontalSpinBox(right_utility=right_utility_button,
                                                                          left_utility=left_utility_button)
        self.horizontal_spinbox.changed.connect(self.spinbox_value)
        
        def spinbox_value(self, value):
            print(value)
            
        def right_function(self):
            self.horizontal_spinbox.spinbox_value = self.horizontal_spinbox.spinbox_value + 10.0

        def left_function(self):
            self.horizontal_spinbox.spinbox_value = self.horizontal_spinbox.spinbox_value - 10.0
"""
