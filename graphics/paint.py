from math import sqrt
from random import randint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphics.extra_messages import *
from graphics.settings_dlg import *
from json_converter import *
from graphics.move_buttons import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_main_window()
        self.create_menu()

        self.__form_widget = FormWidget(self)
        self.setCentralWidget(self.__form_widget)

        self.show()

    def init_main_window(self):
        self.set_geometry()

        self.setWindowTitle('Graph visualisation')
        self.setWindowIcon(QIcon('icons/ui.jpg'))

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

#        settings_act = QAction('Settings', self)
#        settings_act.setStatusTip('Edit application setting')
#        settings_act.triggered.connect(self.create_settings_dlg)

        exit_act = QAction('&Exit', self)
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

#        menu_bar.addAction(settings_act)
        menu_bar.addAction(help_act)

    def open_file(self):
        open_file_dlg = QFileDialog()
        open_file_dlg.setFileMode(QFileDialog.ExistingFile)
        open_file_dlg.setDefaultSuffix('json')
        open_file_dlg.setNameFilter("JSON (*.json)")

        if open_file_dlg.exec_():
            file_name = open_file_dlg.selectedFiles()[0]
            dictionary = read_graph_from_json(file_name)
            self.__form_widget.paint_widget.link_graph(dict_to_graph(dictionary))

    # def create_settings_dlg(self):
    #     draw_param = \
    #         {
    #             'vertex_color': self.vertex_color,
    #             'edge_width': self.edge_width,
    #             'edge_color': self.edge_color,
    #             'font': self.font,
    #             'vertex_label_style': self.vertex_label_style
    #         }
    #     settings_dlg = SettingsDlg(self, draw_param)
    #     settings_dlg.show()

    def help_inf(self):
        ExtraMessages.information_message(self, 'Required format of file', 'Check README file for extra information')


class FormWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.paint_widget = PaintGraphWidget(self)
        self.rbutton = ControlButton(self)
        self.rbutton.right_arrow()
        self.lbutton = ControlButton(self)
        self.lbutton.left_arrow()

        self.__init_layouts()

    def __init_layouts(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.lbutton)
        hbox.addWidget(self.rbutton)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.paint_widget)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def paintEvent(self, event):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(255, 211, 117, 70))
        self.setPalette(palette)


class PaintGraphWidget(QWidget):
    background_color = QColor(255, 211, 117, 60)
    vertex_color = QColor(40, 220, 0)
    vertex_pen = QPen(Qt.black, 1, Qt.SolidLine)
    edge_width = 2
    edge_color = QColor(50, 50, 50)
    font = QFont('Decorative', 10)
    vertex_label_style = 'inside'

    def __init__(self, parent):
        super().__init__(parent)

        self.__h_offsets = {}
        self.__v_offsets = {}

        self.__graph = None
        self.__is_graph_new = False

    def link_graph(self, graph):
        self.__graph = graph
        self.__is_graph_new = True

        self.reset_offsets()
        self.update()

    def reset_offsets(self):
        self.__h_offsets = {}
        self.__v_offsets = {}

    def paintEvent(self, event):
        self.set_bckgrnd_color()

        if not self.__graph:
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

        indent = sqrt((width * height) / self.__graph.vert_amnt)
        radius = indent / 6
        h_num = round((height + radius) / indent)

        if self.__is_graph_new:
            self.set_offsets(indent)
            self.__is_graph_new = False

        i = 0
        j = 0
        points = {}
        for vertex in self.__graph.get_all_vert():
            if j == h_num:
                j = 0
                i += 1
            x = x_0 + i * indent + self.__h_offsets[vertex] + radius
            y = y_0 + j * indent + self.__v_offsets[vertex] + radius
            points[vertex] = [x, y]
            j += 1

        return points, radius

    def set_bckgrnd_color(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.background_color)
        self.setPalette(palette)

    def set_offsets(self, indent):
        for vertex in self.__graph.get_all_vert():
            self.__h_offsets[vertex] = (randint(0, int(indent / 3)))
            self.__v_offsets[vertex] = (randint(0, int(indent / 3)))

    def draw_edges(self, h_painter, points):
        edge_pen = QPen(self.edge_color, self.edge_width, Qt.SolidLine)
        h_painter.setPen(edge_pen)
        for vertex in self.__graph.get_all_vert():
            for adj_vert in self.__graph.get_adj_vert(vertex):
                h_painter.drawLine(points[vertex][0], points[vertex][1]
                                   , points[adj_vert][0], points[adj_vert][1])

    def draw_vertices(self, h_painter, points, radius):
        h_painter.setFont(QFont('Decorative', 10))
        for vertex in self.__graph.get_all_vert():
            x = points[vertex][0] - radius
            y = points[vertex][1] - radius
            h_painter.setBrush(self.vertex_color)
            h_painter.setPen(self.vertex_pen)
            h_painter.drawEllipse(x, y, 2 * radius, 2 * radius)
            h_painter.drawText(QRectF(x, y, 2 * radius, 2 * radius), Qt.AlignCenter, vertex.__str__())
