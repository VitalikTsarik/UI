# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QFont
from PyQt5.QtWidgets import QDialog, QFontDialog, QColorDialog


class SettingsDlg(QDialog):
    def __init__(self, parent, draw_param):
        super(SettingsDlg, self).__init__(parent)
        self.draw_param = draw_param
        self.ui = UiSettingsDlg()
        self.ui.setupUi(self)
        self.connect_actions()
        self.set_cur_state()

    def set_cur_state(self):
        self.ui.tab_widget.setCurrentIndex(0)
        if self.draw_param['vertex_label_style'] == 'inside':
            self.ui.rb_inside.setChecked(True)
        else:
            self.ui.rb_outside.setChecked(True)

        vertex_color = self.draw_param['vertex_color']
        if vertex_color == QColor(120, 120, 255):
            self.ui.rb_vertex_blue.setChecked(True)
        elif vertex_color == QColor(255, 120, 120):
            self.ui.rb_vertex_red.setChecked(True)
        elif vertex_color == QColor(180, 180, 180):
            self.ui.rb_vertex_grey.setChecked(True)

        edge_color = self.draw_param["edge_color"]
        if edge_color == QColor(50, 50, 50):
            self.ui.rb_edge_black.setChecked(True)
        elif edge_color == QColor(120, 120, 255):
            self.ui.rb_edge_blue.setChecked(True)
        elif edge_color == QColor(255, 120, 120):
            self.ui.rb_edge_red.setChecked(True)

        self.ui.spin_box_edge_width.setValue(self.draw_param['edge_width'])

    def connect_actions(self):
        self.ui.rb_inside.toggled.connect(self.rb_inside_action)
        self.ui.rb_outside.toggled.connect(self.rb_outside_action)

        self.ui.btn_change_font.clicked.connect(self.btn_change_font_action)

        self.ui.rb_vertex_blue.toggled.connect(self.rb_vertex_blue_action)
        self.ui.rb_vertex_red.toggled.connect(self.rb_vertex_red_action)
        self.ui.rb_vertex_grey.toggled.connect(self.rb_vertex_grey_action)
        self.ui.btn_vertex_custom_color.clicked.connect(self.btn_vertex_custom_color_action)

        self.ui.rb_edge_blue.toggled.connect(self.rb_edge_blue_action)
        self.ui.rb_edge_red.toggled.connect(self.rb_edge_red_action)
        self.ui.rb_edge_black.toggled.connect(self.rb_edge_black_action)
        self.ui.btn_edge_custom_color.clicked.connect(self.btn_edge_custom_color_action)

        self.ui.standart_btns.accepted.connect(self.accept)
        self.ui.standart_btns.rejected.connect(self.reject)

    def rb_inside_action(self):
        self.draw_param['vertex_label_style'] = 'inside'

    def rb_outside_action(self):
        self.draw_param['vertex_label_style'] = 'outside'

    def btn_change_font_action(self):
        font_dlg = QFontDialog()
        font_dlg.setCurrentFont(self.draw_param['font'])
        if font_dlg.exec_():
            self.draw_param['font'] = font_dlg.currentFont()

    def rb_vertex_blue_action(self):
        self.draw_param['vertex_color'] = QColor(120, 120, 255)

    def rb_vertex_red_action(self):
        self.draw_param['vertex_color'] = QColor(255, 120, 120)

    def rb_vertex_grey_action(self):
        self.draw_param['vertex_color'] = QColor(180, 180, 180)

    def btn_vertex_custom_color_action(self):
        color_dlg = QColorDialog()
        color_dlg.setCurrentColor(self.draw_param['vertex_color'])
        if color_dlg.exec_():
            self.draw_param['vertex_color'] = color_dlg.currentColor()

    def rb_edge_blue_action(self):
        self.draw_param['edge_color'] = QColor(120, 120, 255)

    def rb_edge_red_action(self):
        self.draw_param['edge_color'] = QColor(255, 120, 120)

    def rb_edge_black_action(self):
        self.draw_param['edge_color'] = QColor(50, 50, 50)

    def btn_edge_custom_color_action(self):
        color_dlg = QColorDialog()
        color_dlg.setCurrentColor(self.draw_param['edge_color'])
        if color_dlg.exec_():
            self.draw_param['edge_color'] = color_dlg.currentColor()

    def accept(self):
        self.parent().vertex_label_style = self.draw_param['vertex_label_style']
        self.parent().font = self.draw_param['font']
        self.parent().vertex_color = self.draw_param['vertex_color']
        self.parent().edge_width = self.draw_param['edge_width']
        self.parent().edge_color = self.draw_param['edge_color']
        self.close()


class UiSettingsDlg(object):
    def setupUi(self, settings_dlg):
        settings_dlg.setObjectName("settings_dlg")
        settings_dlg.setEnabled(True)
        settings_dlg.resize(380, 334)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(settings_dlg.sizePolicy().hasHeightForWidth())
        settings_dlg.setSizePolicy(sizePolicy)
        settings_dlg.setSizeGripEnabled(False)
        settings_dlg.setModal(False)
        self.standart_btns = QtWidgets.QDialogButtonBox(settings_dlg)
        self.standart_btns.setGeometry(QtCore.QRect(-120, 300, 491, 21))
        self.standart_btns.setOrientation(QtCore.Qt.Horizontal)
        self.standart_btns.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.standart_btns.setCenterButtons(False)
        self.standart_btns.setObjectName("standart_btns")
        self.tab_widget = QtWidgets.QTabWidget(settings_dlg)
        self.tab_widget.setGeometry(QtCore.QRect(10, 10, 361, 281))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_widget.sizePolicy().hasHeightForWidth())
        self.tab_widget.setSizePolicy(sizePolicy)
        self.tab_widget.setObjectName("tab_widget")
        self.vertex_tab = QtWidgets.QWidget()
        self.vertex_tab.setObjectName("vertex_tab")
        self.groupBox_3 = QtWidgets.QGroupBox(self.vertex_tab)
        self.groupBox_3.setGeometry(QtCore.QRect(240, 10, 101, 161))
        self.groupBox_3.setObjectName("groupBox_3")
        self.btn_vertex_custom_color = QtWidgets.QPushButton(self.groupBox_3)
        self.btn_vertex_custom_color.setGeometry(QtCore.QRect(10, 120, 75, 23))
        self.btn_vertex_custom_color.setObjectName("btn_vertex_custom_color")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox_3)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 81, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rb_vertex_red = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rb_vertex_red.setObjectName("rb_vertex_red")
        self.Color = QtWidgets.QButtonGroup(settings_dlg)
        self.Color.setObjectName("Color")
        self.Color.addButton(self.rb_vertex_red)
        self.verticalLayout.addWidget(self.rb_vertex_red)
        self.rb_vertex_blue = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rb_vertex_blue.setObjectName("rb_vertex_blue")
        self.Color.addButton(self.rb_vertex_blue)
        self.verticalLayout.addWidget(self.rb_vertex_blue)
        self.rb_vertex_grey = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rb_vertex_grey.setObjectName("rb_vertex_grey")
        self.Color.addButton(self.rb_vertex_grey)
        self.verticalLayout.addWidget(self.rb_vertex_grey)
        self.groupBox_2 = QtWidgets.QGroupBox(self.vertex_tab)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 221, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 91, 61))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rb_inside = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.rb_inside.setObjectName("rb_inside")
        self.Label = QtWidgets.QButtonGroup(settings_dlg)
        self.Label.setObjectName("Label")
        self.Label.addButton(self.rb_inside)
        self.verticalLayout_2.addWidget(self.rb_inside)
        self.rb_outside = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.rb_outside.setObjectName("rb_outside")
        self.Label.addButton(self.rb_outside)
        self.verticalLayout_2.addWidget(self.rb_outside)
        self.btn_change_font = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_change_font.setGeometry(QtCore.QRect(120, 40, 75, 23))
        self.btn_change_font.setObjectName("btn_change_font")
        self.tab_widget.addTab(self.vertex_tab, "")
        self.edge_tab = QtWidgets.QWidget()
        self.edge_tab.setObjectName("edge_tab")
        self.label = QtWidgets.QLabel(self.edge_tab)
        self.label.setGeometry(QtCore.QRect(20, 30, 41, 21))
        self.label.setObjectName("label")
        self.spin_box_edge_width = QtWidgets.QSpinBox(self.edge_tab)
        self.spin_box_edge_width.setGeometry(QtCore.QRect(60, 30, 42, 22))
        self.spin_box_edge_width.setMinimum(1)
        self.spin_box_edge_width.setMaximum(5)
        self.spin_box_edge_width.setProperty("value", 2)
        self.spin_box_edge_width.setObjectName("spin_box_edge_width")
        self.groupBox_4 = QtWidgets.QGroupBox(self.edge_tab)
        self.groupBox_4.setGeometry(QtCore.QRect(240, 10, 101, 161))
        self.groupBox_4.setObjectName("groupBox_4")
        self.btn_edge_custom_color = QtWidgets.QPushButton(self.groupBox_4)
        self.btn_edge_custom_color.setGeometry(QtCore.QRect(10, 120, 75, 23))
        self.btn_edge_custom_color.setObjectName("btn_edge_custom_color")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_4)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 81, 91))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.rb_edge_red = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
        self.rb_edge_red.setObjectName("rb_edge_red")
        self.verticalLayout_3.addWidget(self.rb_edge_red)
        self.rb_edge_blue = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
        self.rb_edge_blue.setObjectName("rb_edge_blue")
        self.verticalLayout_3.addWidget(self.rb_edge_blue)
        self.rb_edge_black = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
        self.rb_edge_black.setObjectName("rb_edge_black")
        self.verticalLayout_3.addWidget(self.rb_edge_black)
        self.tab_widget.addTab(self.edge_tab, "")

        self.retranslateUi(settings_dlg)
        QtCore.QMetaObject.connectSlotsByName(settings_dlg)

    def retranslateUi(self, settings_dlg):
        _translate = QtCore.QCoreApplication.translate
        settings_dlg.setWindowTitle(_translate("settings_dlg", "Settings"))
        self.groupBox_3.setTitle(_translate("settings_dlg", "Color"))
        self.btn_vertex_custom_color.setText(_translate("settings_dlg", "Custom"))
        self.rb_vertex_red.setText(_translate("settings_dlg", "Red"))
        self.rb_vertex_blue.setText(_translate("settings_dlg", "Blue"))
        self.rb_vertex_grey.setText(_translate("settings_dlg", "Grey"))
        self.groupBox_2.setTitle(_translate("settings_dlg", "Label"))
        self.rb_inside.setText(_translate("settings_dlg", "Inside"))
        self.rb_outside.setText(_translate("settings_dlg", "Outside"))
        self.btn_change_font.setText(_translate("settings_dlg", "Change font"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.vertex_tab), _translate("settings_dlg", "Vertex"))
        self.label.setText(_translate("settings_dlg", "Width"))
        self.groupBox_4.setTitle(_translate("settings_dlg", "Color"))
        self.btn_edge_custom_color.setText(_translate("settings_dlg", "Custom"))
        self.rb_edge_red.setText(_translate("settings_dlg", "Red"))
        self.rb_edge_blue.setText(_translate("settings_dlg", "Blue"))
        self.rb_edge_black.setText(_translate("settings_dlg", "Black"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.edge_tab), _translate("settings_dlg", "Edge"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    settings_dlg = QtWidgets.QDialog()
    ui = UiSettingsDlg()
    ui.setupUi(settings_dlg)
    settings_dlg.show()
    sys.exit(app.exec_())

