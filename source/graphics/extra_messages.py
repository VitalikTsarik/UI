from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon


class ExtraMessages:
    @staticmethod
    def __initialize_message(window, title, message):
        message_box = QMessageBox(window)
        message_icn = QIcon('source/icons/ui.jpg')
        message_box.setWindowIcon(message_icn)
        message_box.setWindowTitle(title)
        message_box.setText(message)
        return message_box

    @staticmethod
    def error_message(window, title, message):
        err_message = ExtraMessages.__initialize_message(window, title, message)
        err_message.setIcon(QMessageBox.Critical)
        err_message.exec_()

    @staticmethod
    def information_message(window, title, message):
        inf_message = ExtraMessages.__initialize_message(window, title, message)
        inf_message.setIcon(QMessageBox.Information)
        inf_message.exec_()
