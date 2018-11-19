from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


class ControlButton(QPushButton):
    def __init__(self, widget):
        super(ControlButton, self).__init__(widget)

    def __classic_control_button(self):
        self.setStyleSheet("""
                QPushButton {
                    border-radius: 15px;
                    background-color: white;
                    }

                QPushButton:pressed {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                                        stop:0 rgba(255, 255, 255), stop:1 rgba(103, 230, 103, 200))
                    }
                """)
        self.resize(self.width(), self.height() * 1.3)

    def right_arrow(self):
        self.__classic_control_button()
        self.setToolTip('Move forward')
        self.setIcon(QIcon('source/icons/right_arrow'))
        self.setIconSize(QSize(self.height(), self.height()))

    def left_arrow(self):
        self.__classic_control_button()
        self.setToolTip('Move backward')
        self.setIcon(QIcon('source/icons/left_arrow'))
        self.setIconSize(QSize(self.height(), self.height()))
