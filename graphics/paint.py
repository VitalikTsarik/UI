from math import sqrt
from random import randint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphics.extra_messages import *
from graphics.settings_dlg import *
from json_converter import *
from graphics.move_buttons import *
from game_components.game import Game


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.game = Game(self)

        self.init_main_window()
        self.create_menu()

        self.__form_widget = FormWidget(self)
        self.__form_widget.paint_widget.link_graph(self.game.map_graph)
        self.setCentralWidget(self.__form_widget)

        self.show()

        self.__turn_timer = QTimer()
        self.init_turn_timer()

    def init_main_window(self):
        self.set_geometry()

        self.setWindowTitle('Graph visualisation')
        self.setWindowIcon(QIcon('icons/ui.jpg'))

    def set_geometry(self):
        self.resize(1300, 900)
        qr = self.geometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_menu(self):
        help_act = QAction('Help', self)
        help_act.setStatusTip('Show file format')
        help_act.triggered.connect(self.help_inf)

        self.statusBar()
        menu_bar = self.menuBar()

        menu_bar.addAction(help_act)

    def help_inf(self):
        ExtraMessages.information_message(self, 'Help', 'Check README file for extra information')

    def init_turn_timer(self):
        self.__turn_timer.setInterval(10000)
        self.__turn_timer.timeout.connect(self.next_turn)
        self.__turn_timer.start()

    def next_turn(self):
        print('next turn')
        self.game.next_turn()
        self.update()


class FormWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.paint_widget = PaintGraphWidget(self)
        self.rbutton = ControlButton(self)
        self.rbutton.right_arrow()
        self.lbutton = ControlButton(self)
        self.lbutton.left_arrow()
        self.stop_btn = ControlButton(self)
        self.stop_btn.stop()
        self.direction_btns = []
        self.__layouts = []

        self.__init_layouts()

        self.create_dir_btns(range(10))
        self.add_dir_btns()
        self.del_dir_btns()

    def __init_layouts(self):
        hbox_btns_move = QHBoxLayout()
        hbox_btns_move.addWidget(self.lbutton)
        hbox_btns_move.addWidget(self.stop_btn)
        hbox_btns_move.addWidget(self.rbutton)

        hbox_widg = QHBoxLayout()
        hbox_widg.addWidget(self.paint_widget)

        hbox_btns_dir = QHBoxLayout()

        main_vbox = QVBoxLayout(self)
        main_vbox.addLayout(hbox_btns_dir)
        main_vbox.addLayout(hbox_widg)
        main_vbox.addLayout(hbox_btns_move)

        self.__layouts.append(main_vbox)
        self.__layouts.append(hbox_btns_dir)
        self.__layouts.append(hbox_widg)
        self.__layouts.append(hbox_btns_move)

        self.setLayout(main_vbox)

    def create_dir_btns(self, numbers):
        for num in numbers:
            btn = ControlButton(self)
            btn.post_number(num)
            self.direction_btns.append(btn)

    def add_dir_btns(self):
        for btn in self.direction_btns:
            self.__layouts[1].addWidget(btn)

    def del_dir_btns(self):
        while self.__layouts[1].count() > 0:
            self.__layouts[1].takeAt(0).widget().deleteLater()

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
    train_color = QColor(20, 75, 255, 200)
    train_size = 20

    def __init__(self, parent):
        super().__init__(parent)

        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

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
        self.draw_trains(h_painter, self.parent().parent().game.trains, points)

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
        for vertex in self.__graph.get_all_vertices():
            if j == h_num:
                j = 0
                i += 1
            x = x_0 + i * indent + self.__h_offsets[vertex] + radius
            y = y_0 + j * indent + self.__v_offsets[vertex] + radius
            points[vertex] = QPointF(x, y)
            j += 1

        return points, radius

    def set_bckgrnd_color(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.background_color)
        self.setPalette(palette)

    def set_offsets(self, indent):
        for vertex in self.__graph.get_all_vertices():
            self.__h_offsets[vertex] = (randint(0, int(indent / 3)))
            self.__v_offsets[vertex] = (randint(0, int(indent / 3)))

    def draw_edges(self, h_painter, points):
        edge_pen = QPen(self.edge_color, self.edge_width, Qt.SolidLine)
        h_painter.setPen(edge_pen)
        for vertex in self.__graph.get_all_vertices():
            for adj_vert in self.__graph.get_adj_vertices(vertex):
                h_painter.drawLine(points[vertex], points[adj_vert])

    def draw_vertices(self, h_painter, points, radius):
        h_painter.setFont(QFont('Decorative', 10))
        for vertex in self.__graph.get_all_vertices():
            x = points[vertex].x() - radius
            y = points[vertex].y() - radius
            h_painter.setBrush(self.vertex_color)
            h_painter.setPen(self.vertex_pen)
            h_painter.drawEllipse(x, y, 2 * radius, 2 * radius)
            h_painter.drawText(QRectF(x, y, 2 * radius, 2 * radius), Qt.AlignCenter, vertex.__str__())

    def draw_trains(self, h_painter, trains, points):
        h_painter.setBrush(self.train_color)
        for train in trains:
            self.draw_train(h_painter, train, points)

    def draw_train(self, h_painter, train, points):
        edge = self.__graph.get_edge_by_idx(train.line_idx)
        p1 = points[edge['vert1']]
        p2 = points[edge['vert2']]
        length = edge['length']
        a, b = self.calc_line(p1, p2)
        cx = p1.x() + (train.position/length)*(p2.x() - p1.x())
        cy = a*cx + b
        h_painter.drawRect(cx - self.train_size, cy - self.train_size, self.train_size*2, self.train_size*2)

    def calc_line(self, p1, p2):
        a = (p2.y() - p1.y())/(p2.x() - p1.x())
        b = p1.y() - a*p1.x()
        return a, b
