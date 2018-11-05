from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QIcon


class ErrorWindow:
    def __init__(self, window):
        self._window = window

    def call_error_window(self, error_message, error_details=None):
        err_box = QMessageBox(self._window)
        err_icon = QIcon('icons/error.png')
        err_box.setWindowIcon(err_icon)
        err_box.setWindowTitle('Error')
        err_box.setIcon(QMessageBox.Critical)
        err_box.setText(error_message)
        if error_details:
            err_box.setInformativeText(error_details)
        err_box.exec_()
