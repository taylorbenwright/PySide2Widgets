from PySide2.QtWidgets import QFrame


class BoxLayoutSeparator(QFrame):

    def __init__(self, direction, *args, **kwargs):
        """
        Creates a shallow separator for a BoxLayout to use.
        :param direction: Which direction this separator should go
        :type direction: QFrame.Shape
        """
        super(BoxLayoutSeparator, self).__init__(*args, **kwargs)
        self.setFrameShape(direction)
        self.setFrameShadow(QFrame.Sunken)
