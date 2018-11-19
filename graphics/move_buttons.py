from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import QSize


class ControlButton(QPushButton):
    def __init__(self, widget=None):
        super(ControlButton, self).__init__(widget)

    def __arrow(self, tool_tip, icon_path):
        self.resize(self.width(), self.height() * 1.3)
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
        self.setToolTip(tool_tip)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(self.height(), self.height()))

    def right_arrow(self):
        self.__arrow('Move forward', 'icons/right_arrow')

    def left_arrow(self):
        self.__arrow('Move backward', 'icons/left_arrow')

    def post_number(self, number):
        self.setToolTip(f'Move to {number}')
        self.setText(f'{number}')
        self.setFont(QFont('Times', 14))
        self.setStyleSheet("""
                        QPushButton {
                            border: 1px solid-black;
                            border-radius: 15px;
                            background-color: white;
                            width: 60px;
                            }
        
                        QPushButton:pressed {
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                        stop:0 rgba(255, 255, 255), stop:1 rgba(103, 230, 103, 200))
                            }
                         """)
