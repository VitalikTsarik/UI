# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QTableWidgetItem


class FindGameDlg(QDialog):
    def __init__(self, lobbies, parent=None):
        super(FindGameDlg, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('source/icons/icon.png'))

        self.__lobbies = lobbies
        self.name = ''
        self.num_players = 1
        self.num_turns = -1
        self.state = 2
        self.init_table()

    def init_table(self):
        n = len(self.__lobbies)
        self.ui.table.setRowCount(n)
        for i in range(n):
            lobby = self.__lobbies[i]
            self.ui.table.setItem(i, 0, QTableWidgetItem(lobby.name))
            self.ui.table.setItem(i, 1, QTableWidgetItem(str(lobby.num_players)))
            self.ui.table.setItem(i, 2, QTableWidgetItem(str(lobby.num_turns)))
            self.ui.table.setItem(i, 3, QTableWidgetItem(lobby.state))

    def submit(self):
        row = self.ui.table.selectedItems()
        self.name = row[0]
        self.num_players = row[1]
        self.num_turns = row[2]
        self.state = row[3]
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

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

