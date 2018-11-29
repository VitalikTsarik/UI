from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from source.graphics.move_buttons import ControlButton

class ExtraMessages:
    @staticmethod
    def __initialize_message(pwindow, title, message):
        message_box = QMessageBox(pwindow)
        message_icn = QIcon('icons/ui.jpg')
        message_box.setWindowIcon(message_icn)
        message_box.setWindowTitle(title)
        message_box.setText(message)
        return message_box

    @staticmethod
    def error_message(pwindow, title, message):
        err_message = ExtraMessages.__initialize_message(pwindow, title, message)
        err_message.setIcon(QMessageBox.Critical)
        err_message.exec_()

    @staticmethod
    def information_message(pwindow, title, message):
        inf_message = ExtraMessages.__initialize_message(pwindow, title, message)
        inf_message.setIcon(QMessageBox.Information)
        inf_message.exec_()

    @staticmethod
    def button_dialog(numbers, pwindow):
        btn_dlg = ExtraMessages.__initialize_message(pwindow, 'Move', 'Select which point you want to move')

        for num in numbers:
            btn = ControlButton(btn_dlg)
            btn.post_number(num)
            btn_dlg.addButton(btn, QMessageBox.NoRole)
        btn_dlg.show()
