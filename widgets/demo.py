import random
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import SIGNAL, Signal, Qt
import ps2_BoxLayoutSeparator
import ps2_HorizontalSpinBox
import ps2_EditableLabel
import ps2_FillLineButton
import ps2_FillListButton
import ps2_MayaSpinBox
import ps2_RenameList
import ps2_TristateCheckbox
import ps2_Rollout
import ps2_ColorSwatch
import sys


class Demo(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Demo, self).__init__(parent=parent)

        self.setWindowTitle('PySide2 Widgets Demo')

        self.generate_ui()
        self.show()

    def generate_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        grid_layout = QtWidgets.QGridLayout()

        row = 0

        # Horizontal Spin Box with utility functions
        right_function = {
            'label': '>>',
            'function': self.horizontal_spinbox_function
        }

        left_function = {
            'label': '<<',
            'function': self.horizontal_spinbox_function
        }

        hsb_label = QtWidgets.QLabel('Horizontal Spin Box:')
        self.hsb_widget = ps2_HorizontalSpinBox.HorizontalSpinBox(left_utility=left_function,
                                                                  right_utility=right_function)
        grid_layout.addWidget(hsb_label, row, 0)
        grid_layout.addLayout(self.hsb_widget, row, 1)
        row += 1

        row = self.add_separator_row(grid_layout, row)

        # Editable Label
        edl_label = QtWidgets.QLabel('Editable Label:')
        self.edl_widget = ps2_EditableLabel.EditableLabel("Double Click me!")
        grid_layout.addWidget(edl_label, row, 0)
        grid_layout.addWidget(self.edl_widget, row, 1)
        row += 1

        row = self.add_separator_row(grid_layout, row)

        # Fill Line Button
        flb_label = QtWidgets.QLabel('Fill Line Button:')
        self.flb_widget = ps2_FillLineButton.FillLineButton(empty_text="Type something here, press the button, and watch your console!")
        self.flb_widget.clicked.connect(self.fill_line_button_clicked)
        grid_layout.addWidget(flb_label, row, 0)
        grid_layout.addWidget(self.flb_widget, row, 1)
        row += 1

        row = self.add_separator_row(grid_layout, row)

        # Fill List Button
        flsb_label = QtWidgets.QLabel('Fill List Button:')
        flsb_layout = QtWidgets.QVBoxLayout()
        self.fill_list_etb = QtWidgets.QLineEdit()
        self.fill_list_etb.setPlaceholderText('Type something, then press <<')
        self.flsb_widget = ps2_FillListButton.FillListButton()
        self.flsb_widget.clicked.connect(self.fill_list_button_clicked)
        flsb_layout.addWidget(self.fill_list_etb)
        flsb_layout.addWidget(self.flsb_widget)
        grid_layout.addWidget(flsb_label, row, 0)
        grid_layout.addLayout(flsb_layout, row, 1)
        row += 1

        row = self.add_separator_row(grid_layout, row)

        # Maya Spinbox
        msb_label = QtWidgets.QLabel('Maya Spinbox:')
        msb_widget = ps2_MayaSpinBox.MayaSpinbox()
        grid_layout.addWidget(msb_label, row, 0)
        grid_layout.addWidget(msb_widget, row, 1)
        row += 1

        row = self.add_separator_row(grid_layout, row)

        # Rename List
        starting_list = [
            'This', 'Is', 'A', 'Rename', 'List'
        ]
        rl_label = QtWidgets.QLabel('Rename List:')
        rl_widget = ps2_RenameList.RenameList(starting_list)
        grid_layout.addWidget(rl_label, row, 0)
        grid_layout.addWidget(rl_widget, row, 1)
        row += 1

        row = self.add_separator_row(grid_layout, row)

        # Tristate Checkbox
        tscbx_label = QtWidgets.QLabel('Tristate Checkbox:')
        tscbx_widget = ps2_TristateCheckbox.TristateCheckbox()
        tscbx_widget.setCheckState(Qt.PartiallyChecked)
        grid_layout.addWidget(tscbx_label, row, 0)
        grid_layout.addWidget(tscbx_widget, row, 1)
        row += 1

        row = self.add_separator_row(grid_layout, row)

        # Rollout
        content_layout = QtWidgets.QVBoxLayout()
        for ind in range(5):
            wid = QtWidgets.QPushButton(str(ind))
            content_layout.addWidget(wid)
        rollout_label = QtWidgets.QLabel('Rollout:')
        rollout_widget = ps2_Rollout.Rollout(label='Rollout Title', border=True, content=content_layout)
        grid_layout.addWidget(rollout_label, row, 0)
        grid_layout.addWidget(rollout_widget, row, 1)
        row += 1

        row = self.add_separator_row(grid_layout, row)

        # Color Swatch
        cw_layout = QtWidgets.QHBoxLayout()
        for i in range(5):
            color = QtGui.QColor()
            color.setRgb(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            swatch = ps2_ColorSwatch.ColorSwatch(color)
            swatch.clicked.connect(self.print_color)
            cw_layout.addWidget(swatch)
        cw_label = QtWidgets.QLabel('Color Swatch:')
        grid_layout.addWidget(cw_label, row, 0)
        grid_layout.addLayout(cw_layout, row, 1)
        row += 1

        row = self.add_separator_row(grid_layout, row)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    @staticmethod
    def horizontal_separator() -> ps2_BoxLayoutSeparator.BoxLayoutSeparator:
        return ps2_BoxLayoutSeparator.BoxLayoutSeparator(direction=QtWidgets.QFrame.Shape.HLine)

    @staticmethod
    def add_separator_row(grid_layout, row) -> int:
        grid_layout.addWidget(QtWidgets.QWidget(), row, 0)
        grid_layout.addWidget(Demo.horizontal_separator(), row, 1)
        return row + 1

    def horizontal_spinbox_function(self):
        sender = self.sender()
        match sender:
            case self.hsb_widget.left_utility:
                self.hsb_widget.spinbox_value -= 10
            case self.hsb_widget.right_utility:
                self.hsb_widget.spinbox_value += 10

    def fill_line_button_clicked(self, line_edit_text: str):
        print(line_edit_text)

    def fill_list_button_clicked(self):
        self.flsb_widget.add_value_to_list(self.fill_list_etb.text())
        self.fill_list_etb.setText('')

    def print_color(self):
        sender = self.sender()  # type: ps2_ColorSwatch.ColorSwatch
        red, green, blue = sender.color.red(), sender.color.green(), sender.color.blue()
        print(f"Red: {red}, Green: {green}, Blue: {blue}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Demo()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()