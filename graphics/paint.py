from math import sqrt
from random import randint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphics.extra_messages import *
from json_converter import *


class MainWindow(QMainWindow):
    def __init__(self):
        # todo: instance_of Graph
        super().__init__()

        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)
        self.init_ui()
        # ExtraMessages.information_message(self, "Get started", "To choose the file with your graph select:\nFile->Open...")

    def init_ui(self):
        self.set_geometry()

        self.setWindowTitle('Graph visualisation')
        self.setWindowIcon(QIcon('icons/ui.jpg'))

        self.create_menu()
        self.show()

    def set_geometry(self):
        self.resize(1300, 900)
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        qr = self.geometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_menu(self):
        new_act = QAction('Open...', self)
        new_act.setStatusTip('Open a file with graph')
        new_act.triggered.connect(self.open_file)

        settings_act = QAction('Settings', self)
        settings_act.setStatusTip('Edit application setting')
        settings_act.triggered.connect(self.create_settings_dlg)

        exit_act = QAction('&Exit', self)  # QtGui.QIcon('exit.png'),
        exit_act.setStatusTip('Quit application')
        exit_act.triggered.connect(qApp.quit)

        help_act = QAction('Help', self)
        help_act.setStatusTip('Show file format')
        help_act.triggered.connect(self.help_inf)

        self.statusBar()
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(new_act)
        file_menu.addSeparator()
        file_menu.addAction(exit_act)

        menu_bar.addAction(settings_act)
        menu_bar.addAction(help_act)

    def open_file(self):
        open_file_dlg = QFileDialog()
        open_file_dlg.setFileMode(QFileDialog.ExistingFile)
        open_file_dlg.setDefaultSuffix('json')
        open_file_dlg.setNameFilter("JSON (*.json)")

        if open_file_dlg.exec_():
            file_name = open_file_dlg.selectedFiles()[0]
            dictionary = read_graph_from_json(file_name)
            try:
                self.form_widget.link_graph(dict_to_graph(dictionary))
            except KeyError:
                ExtraMessages.error_message(self, 'Data error', 'Please, check the format of data in your json file')

    def create_settings_dlg(self):
        settings_dlg = QDialog()
        ui = SettingsDlgUi()
        ui.setupUi(settings_dlg)
        settings_dlg.show()
        settings_dlg.exec_()

    def help_inf(self):
        ExtraMessages.information_message(self, 'Required format of file', 'Check README file for extra information')


class FormWidget(QWidget):
    circles_color = QColor(120, 120, 255)
    circles_pen = QPen(Qt.black, 1, Qt.SolidLine)
    lines_pen = QPen(QColor(100, 100, 100), 2, Qt.SolidLine)
    font = QFont('Decorative', 10)

    def __init__(self, parent):
        # todo: может это старый синтаксис
        super(FormWidget, self).__init__(parent)
        self.create_button()
        self.graph = None
        self.is_graph_new = None

    def create_button(self):
        ok_btn = QPushButton('OK')
        ok_btn.clicked.connect(qApp.quit)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_btn)

        vbox = QVBoxLayout(self)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    @property
    def is_graph_new(self):
        return self._is_graph_new

    @is_graph_new.setter
    def is_graph_new(self, value: bool):
        self._is_graph_new = value

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, value: Graph):
        self._graph = value

    def link_graph(self, graph):
        self.graph = graph
        self.is_graph_new = True
        self.reset_offsets()
        self.update()

    def reset_offsets(self):
        self.h_offsets = {}
        self.v_offsets = {}

    def paintEvent(self, event):
        if not self.graph:
            return

        points, radius = self.calc_coordinates()

        h_painter = QPainter()
        h_painter.begin(self)

        self.draw_edges(h_painter, points)
        self.draw_vertices(h_painter, points, radius)

        h_painter.end()

    # todo: подумать(или нет)
    def calc_coordinates(self):
        padding = 50
        x_0 = padding
        y_0 = padding

        width = self.frameGeometry().width() - padding * 4
        height = self.frameGeometry().height() - padding * 4

        indent = sqrt((width * height) / self.graph.vert_amnt)
        radius = indent / 6
        h_num = round((height + radius) / indent)

        if self.is_graph_new:
            self.set_offsets(indent)
            self.is_graph_new = False

        i = 0
        j = 0
        points = {}
        for vertex in self.graph.get_all_vert():
            if j == h_num:
                j = 0
                i += 1
            x = x_0 + i * indent + self.h_offsets[vertex] + radius
            y = y_0 + j * indent + self.v_offsets[vertex] + radius
            points[vertex] = [x, y]
            j += 1

        return points, radius

    def set_offsets(self, indent):
        for vertex in self.graph.get_all_vert():
            self.h_offsets[vertex] = (randint(0, int(indent / 3)))
            self.v_offsets[vertex] = (randint(0, int(indent / 3)))

    def draw_edges(self, h_painter, points):
        h_painter.setPen(self.lines_pen)
        for vertex in self.graph.get_all_vert():
            for adj_vert in self.graph.get_adj_edge(vertex):
                h_painter.drawLine(points[vertex][0], points[vertex][1]
                                   , points[adj_vert["vert_to"]][0], points[adj_vert["vert_to"]][1])

    def draw_vertices(self, h_painter, points, radius):
        h_painter.setFont(self.font)
        for vertex in self.graph.get_all_vert():
            x = points[vertex][0] - radius
            y = points[vertex][1] - radius

            # h_painter.setBrush(Qt.NoBrush)
            # h_painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            # h_painter.drawEllipse(x - self.h_points_offsets[vertex], y - self.v_points_offsets[vertex], 2*radius, 2*radius)
            # h_painter.drawText(QRectF(x - self.h_points_offsets[vertex], y - self.v_points_offsets[vertex]
            #                    , 2*radius, 2*radius), Qt.AlignCenter, vertex.__str__())

            h_painter.setBrush(self.circles_color)
            h_painter.setPen(self.circles_pen)
            h_painter.drawEllipse(x, y, 2 * radius, 2 * radius)
            h_painter.drawText(QRectF(x, y, 2 * radius, 2 * radius), Qt.AlignCenter, vertex.__str__())


class SettingsDlgUi(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(380, 334)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(-130, 300, 491, 21))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setGeometry(QRect(10, 10, 361, 281))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.groupBox_3 = QGroupBox(self.tab)
        self.groupBox_3.setGeometry(QRect(240, 10, 101, 161))
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton = QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QRect(10, 120, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayoutWidget = QWidget(self.groupBox_3)
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 81, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton = QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.Color = QButtonGroup(Dialog)
        self.Color.setObjectName("Color")
        self.Color.addButton(self.radioButton)
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.Color.addButton(self.radioButton_2)
        self.verticalLayout.addWidget(self.radioButton_2)
        self.radioButton_3 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_3.setObjectName("radioButton_3")
        self.Color.addButton(self.radioButton_3)
        self.verticalLayout.addWidget(self.radioButton_3)
        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QRect(10, 10, 221, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget_2 = QWidget(self.groupBox_2)
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 91, 61))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButton_4 = QRadioButton(self.verticalLayoutWidget_2)
        self.radioButton_4.setObjectName("radioButton_4")
        self.Label = QButtonGroup(Dialog)
        self.Label.setObjectName("Label")
        self.Label.addButton(self.radioButton_4)
        self.verticalLayout_2.addWidget(self.radioButton_4)
        self.radioButton_5 = QRadioButton(self.verticalLayoutWidget_2)
        self.radioButton_5.setObjectName("radioButton_5")
        self.Label.addButton(self.radioButton_5)
        self.verticalLayout_2.addWidget(self.radioButton_5)
        self.pushButton_2 = QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QRect(120, 40, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label = QLabel(self.tab_2)
        self.label.setGeometry(QRect(20, 30, 41, 21))
        self.label.setObjectName("label")
        self.spinBox = QSpinBox(self.tab_2)
        self.spinBox.setGeometry(QRect(60, 30, 42, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(5)
        self.spinBox.setProperty("value", 2)
        self.spinBox.setObjectName("spinBox")
        self.groupBox_4 = QGroupBox(self.tab_2)
        self.groupBox_4.setGeometry(QRect(240, 10, 101, 161))
        self.groupBox_4.setObjectName("groupBox_4")
        self.pushButton_3 = QPushButton(self.groupBox_4)
        self.pushButton_3.setGeometry(QRect(10, 120, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayoutWidget_3 = QWidget(self.groupBox_4)
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 20, 81, 91))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radioButton_6 = QRadioButton(self.verticalLayoutWidget_3)
        self.radioButton_6.setObjectName("radioButton_6")
        self.verticalLayout_3.addWidget(self.radioButton_6)
        self.radioButton_7 = QRadioButton(self.verticalLayoutWidget_3)
        self.radioButton_7.setObjectName("radioButton_7")
        self.verticalLayout_3.addWidget(self.radioButton_7)
        self.radioButton_8 = QRadioButton(self.verticalLayoutWidget_3)
        self.radioButton_8.setObjectName("radioButton_8")
        self.verticalLayout_3.addWidget(self.radioButton_8)
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.groupBox_3.setTitle(_translate("Dialog", "Color"))
        self.pushButton.setText(_translate("Dialog", "Custom"))
        self.radioButton.setText(_translate("Dialog", "Red"))
        self.radioButton_2.setText(_translate("Dialog", "Blue"))
        self.radioButton_3.setText(_translate("Dialog", "Black"))
        self.groupBox_2.setTitle(_translate("Dialog", "Label"))
        self.radioButton_4.setText(_translate("Dialog", "Inside"))
        self.radioButton_5.setText(_translate("Dialog", "Outside"))
        self.pushButton_2.setText(_translate("Dialog", "Change font"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Vertex"))
        self.label.setText(_translate("Dialog", "Width"))
        self.groupBox_4.setTitle(_translate("Dialog", "Color"))
        self.pushButton_3.setText(_translate("Dialog", "Custom"))
        self.radioButton_6.setText(_translate("Dialog", "Red"))
        self.radioButton_7.setText(_translate("Dialog", "Blue"))
        self.radioButton_8.setText(_translate("Dialog", "Black"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Edge"))

