from math import sqrt
from random import randint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphics.extra_messages import *
from graphics.settings_dlg import *
from json_converter import *


class MainWindow(QMainWindow):
    vertex_color = QColor(120, 120, 255)
    vertex_pen = QPen(Qt.black, 1, Qt.SolidLine)
    edge_width = 2
    edge_color = QColor(100, 100, 100)
    font = QFont('Decorative', 10)
    vertex_label_style = 'inside'

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
        draw_param = \
            {
                'vertex_color': self.vertex_color,
                'edge_width': self.edge_width,
                'edge_color': self.edge_color,
                'font': self.font,
                'vertex_label_style': self.vertex_label_style
            }
        settings_dlg = SettingsDlg(self, draw_param)
        settings_dlg.show()
        self.update()

    def help_inf(self):
        ExtraMessages.information_message(self, 'Required format of file', 'Check README file for extra information')


class FormWidget(QWidget):

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
        edge_pen = QPen(self.parent().edge_color, self.parent().edge_width, Qt.SolidLine)
        h_painter.setPen(edge_pen)
        for vertex in self.graph.get_all_vert():
            for adj_vert in self.graph.get_adj_edge(vertex):
                h_painter.drawLine(points[vertex][0], points[vertex][1]
                                   , points[adj_vert["vert_to"]][0], points[adj_vert["vert_to"]][1])

    def draw_vertices(self, h_painter, points, radius):
        h_painter.setFont(self.parent().font)
        for vertex in self.graph.get_all_vert():
            x = points[vertex][0] - radius
            y = points[vertex][1] - radius

            # h_painter.setBrush(Qt.NoBrush)
            # h_painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            # h_painter.drawEllipse(x - self.h_points_offsets[vertex], y - self.v_points_offsets[vertex], 2*radius, 2*radius)
            # h_painter.drawText(QRectF(x - self.h_points_offsets[vertex], y - self.v_points_offsets[vertex]
            #                    , 2*radius, 2*radius), Qt.AlignCenter, vertex.__str__())

            h_painter.setBrush(self.parent().vertex_color)
            h_painter.setPen(self.parent().vertex_pen)
            h_painter.drawEllipse(x, y, 2 * radius, 2 * radius)
            h_painter.drawText(QRectF(x, y, 2 * radius, 2 * radius), Qt.AlignCenter, vertex.__str__())

