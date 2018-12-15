# -*- coding: utf-8 -*-

# Created by: PyQt5 UI code generator 5.11.3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QPen, QFont, QIcon
from PyQt5.QtWidgets import QDialog, QFontDialog, QColorDialog, QDialogButtonBox


class NewGameDlg(QDialog):
    def __init__(self, parent=None):
        super(NewGameDlg, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('source/icons/icon.png'))
        self.connect_actions()

        self.player_name = ''
        self.game_name = ''
        self.num_players = 1
        self.num_turns = -1

    def connect_actions(self):
        self.ui.cb_infinite.clicked.connect(self.cb_infinite_clicked)

    def cb_infinite_clicked(self):
        if self.sender().isChecked():
            self.ui.sb_num_turns.setEnabled(False)
        else:
            self.ui.sb_num_turns.setEnabled(True)

    def submit(self):
        self.player_name = self.ui.player_name.text()
        self.game_name = self.ui.game_name.text()
        self.num_turns = self.ui.sb_num_turns.value()
        if self.ui.cb_infinite.isChecked():
            self.num_turns = -1
        else:
            self.num_turns = self.ui.sb_num_turns.value()
        self.num_players = self.ui.sb_num_players.value()
        self.accept()

# Created by: PyQt5 UI code generator 5.11.3

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(229, 248)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setAutoFillBackground(False)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-10, 210, 231, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 211, 191))
        self.groupBox.setObjectName("groupBox")
        self.player_name = QtWidgets.QLineEdit(self.groupBox)
        self.player_name.setGeometry(QtCore.QRect(90, 30, 113, 20))
        self.player_name.setObjectName("player_name")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 71, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 71, 21))
        self.label_2.setObjectName("label_2")
        self.game_name = QtWidgets.QLineEdit(self.groupBox)
        self.game_name.setGeometry(QtCore.QRect(90, 60, 113, 20))
        self.game_name.setObjectName("game_name")
        self.sb_num_turns = QtWidgets.QSpinBox(self.groupBox)
        self.sb_num_turns.setEnabled(False)
        self.sb_num_turns.setGeometry(QtCore.QRect(110, 100, 42, 22))
        self.sb_num_turns.setObjectName("sb_num_turns")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 91, 21))
        self.label_3.setObjectName("label_3")
        self.cb_infinite = QtWidgets.QCheckBox(self.groupBox)
        self.cb_infinite.setGeometry(QtCore.QRect(110, 130, 70, 17))
        self.cb_infinite.setChecked(True)
        self.cb_infinite.setObjectName("cb_infinite")
        self.sb_num_players = QtWidgets.QSpinBox(self.groupBox)
        self.sb_num_players.setEnabled(True)
        self.sb_num_players.setGeometry(QtCore.QRect(110, 160, 42, 22))
        self.sb_num_players.setProperty("value", 1)
        self.sb_num_players.setObjectName("sb_num_players")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 91, 21))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.submit)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "New Game"))
        self.groupBox.setTitle(_translate("Dialog", "Game Parameters"))
        self.label.setText(_translate("Dialog", "Player\'s name:"))
        self.label_2.setText(_translate("Dialog", "Game\'s name:"))
        self.label_3.setText(_translate("Dialog", "Number of turns:"))
        self.cb_infinite.setText(_translate("Dialog", "infinite"))
        self.label_4.setText(_translate("Dialog", "Number of players:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = NewGameDlg()

    Dialog.show()
    sys.exit(app.exec_())

