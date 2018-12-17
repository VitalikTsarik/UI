# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QDialogButtonBox

from game_components.lobby import Lobby, GameState


class FindGameDlg(QDialog):
    def __init__(self, lobbies, parent=None):
        super(FindGameDlg, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.setWindowIcon(QIcon('source\icons\icon.png'))

        self.__lobbies = lobbies
        self.lobby = None
        self.player_name = None
        self.init_table()
        self.ui.table.itemSelectionChanged.connect(lambda:
                                                   self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True))

    def init_table(self):
        n = len(self.__lobbies)
        self.ui.table.setRowCount(n)
        i = 0
        for lobby in self.__lobbies.values():
            self.ui.table.setItem(i, 0, QTableWidgetItem(lobby.name))
            self.ui.table.setItem(i, 1, QTableWidgetItem(str(lobby.num_players)))
            if lobby.num_turns < 0:
                self.ui.table.setItem(i, 2, QTableWidgetItem('infinite'))
            else:
                self.ui.table.setItem(i, 2, QTableWidgetItem(str(lobby.num_turns)))
            if lobby.state == GameState.INIT.value:
                self.ui.table.setItem(i, 3, QTableWidgetItem('initialization'))
            elif lobby.state == GameState.RUN.value:
                self.ui.table.setItem(i, 3, QTableWidgetItem('running'))
            elif lobby.state == GameState.FINISHED.value:
                self.ui.table.setItem(i, 3, QTableWidgetItem('finished'))
            i += 1

    def submit(self):
        row = self.ui.table.selectedItems()
        if row[2].text() == 'infinite':
            num_turns = -1
        else:
            num_turns = int(row[2].text())
        if row[3].text() == 'initialization':
            state = GameState.INIT.value
        elif row[3].text() == 'running':
            state = GameState.RUN.value
        else:
            state = GameState.FINISHED.value
        self.lobby = Lobby(row[0].text(), int(row[1].text()), num_turns, state)
        self.player_name = self.ui.le_player_name.text()
        self.accept()

# Created by: PyQt5 UI code generator 5.11.3


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(535, 250)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(535, 250))
        Dialog.setMaximumSize(QtCore.QSize(535, 250))
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(160, 210, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.table = QtWidgets.QTableWidget(Dialog)
        self.table.setGeometry(QtCore.QRect(10, 10, 521, 192))
        self.table.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setTextElideMode(QtCore.Qt.ElideRight)
        self.table.setShowGrid(False)
        self.table.setGridStyle(QtCore.Qt.SolidLine)
        self.table.setWordWrap(True)
        self.table.setCornerButtonEnabled(True)
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setObjectName("table")
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setKerning(False)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setCascadingSectionResizes(False)
        self.table.horizontalHeader().setDefaultSectionSize(120)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.horizontalHeader().setSortIndicatorShown(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(True)
        self.table.verticalHeader().setCascadingSectionResizes(False)
        self.table.verticalHeader().setDefaultSectionSize(30)
        self.table.verticalHeader().setHighlightSections(True)
        self.table.verticalHeader().setSortIndicatorShown(False)
        self.table.verticalHeader().setStretchLastSection(False)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 215, 71, 31))
        self.label.setObjectName("label")
        self.le_player_name = QtWidgets.QLineEdit(Dialog)
        self.le_player_name.setGeometry(QtCore.QRect(90, 220, 131, 20))
        self.le_player_name.setObjectName("le_player_name")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.submit)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Find"))
        self.table.setSortingEnabled(False)
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Name"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Number of players"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Number of turns"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "State"))
        self.label.setText(_translate("Dialog", "Player Name:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

