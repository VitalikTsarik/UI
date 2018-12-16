from math import sqrt
from random import randint

from source.graphics.move_buttons import ControlButton
from source.game_components.game import Game
from source.game_components.lobby import Lobby, GameState
from source.graphics.extra_messages import ExtraMessages
from source.graphics.new_game_dlg import NewGameDlg
from source.graphics.find_game_dlg import FindGameDlg

from PyQt5.QtCore import QRectF, QTimer, QPointF, QLineF, Qt
from PyQt5.QtGui import QPainter, QPixmap, QColor, QIcon, QPen, QFont
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget, QHBoxLayout, QVBoxLayout, QAction, qApp


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.game = Game()

        self.init_main_window()
        self.create_menu()

        self.__form_widget = FormWidget(self)

        self.setCentralWidget(self.__form_widget)

        self.show()

        self.__turn_timer = QTimer()
        self.__wait_players_timer = QTimer()
        self.init_timers()

    def init_main_window(self):
        self.set_geometry()

        self.setWindowTitle('World of Wartrains')
        self.setWindowIcon(QIcon('source/icons/icon.png'))

    def set_geometry(self):
        self.resize(900, 1000)

        qr = self.geometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_menu(self):
        new_act = QAction('&New...', self)
        new_act.setStatusTip('Create a new game')
        new_act.triggered.connect(self.new_game)

        find_act = QAction('&Find...', self)
        find_act.setStatusTip('Find and connect to existing game')
        find_act.triggered.connect(self.find_game)

        exit_act = QAction('&Exit', self)
        exit_act.setStatusTip('Quit application')
        exit_act.triggered.connect(qApp.quit)

        self.statusBar()
        menu_bar = self.menuBar()

        game_menu = menu_bar.addMenu('&Game')
        game_menu.addAction(new_act)
        game_menu.addAction(find_act)
        game_menu.addSeparator()
        game_menu.addAction(exit_act)

    def new_game(self):
        dlg = NewGameDlg(self)
        if dlg.exec_():
            self.__turn_timer.stop()
            self.centralWidget().next_turn_btn.setEnabled(False)
            self.game.new_game(dlg.player_name, dlg.lobby)
            self.__form_widget.paint_widget.link_graph(self.game.map_graph)
            self.repaint()

            self.__wait_players_timer.start()

    def find_game(self):
        dlg = FindGameDlg(self.game.get_existing_games(), self)
        if dlg.exec_():
            self.__turn_timer.stop()
            self.game.connect_to_game(dlg.player_name, dlg.lobby)
            self.centralWidget().next_turn_btn.setEnabled(False)
            self.__form_widget.paint_widget.link_graph(self.game.map_graph)
            self.repaint()
            self.__wait_players_timer.start()

    def init_timers(self):
        self.__turn_timer.setInterval(10000)
        self.__turn_timer.timeout.connect(self.next_turn)
        self.__wait_players_timer.setInterval(100)
        self.__wait_players_timer.timeout.connect(self.wait_other_player)

    def next_turn(self):
        print('next turn')
        res = self.game.next_turn()
        if res == -1:
            ExtraMessages.information_message(self, 'Game Over', 'Game Over')
            self.__turn_timer.stop()
        self.update()

    def next_turn_btn_clicked(self):
        self.game.next_turn_action()
        self.next_turn()
        self.__turn_timer.start()

    def wait_other_player(self):
        if self.game.lobby.state != GameState.RUN.value:
            self.game.lobby = self.game.get_existing_games()[self.game.lobby.name]
        else:
            self.centralWidget().next_turn_btn.setEnabled(True)
            self.__turn_timer.start()
            self.game.start_game()
            self.__wait_players_timer.stop()


class FormWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.paint_widget = PaintGraphWidget(self)
        self.next_turn_btn = ControlButton(self)
        self.next_turn_btn.resize(50, 50)
        self.next_turn_btn.next_turn()
        self.next_turn_btn.setEnabled(False)
        self.next_turn_btn.clicked.connect(self.parent().next_turn_btn_clicked)

        self.__layouts = []
        self.__init_layouts()

    def __init_layouts(self):
        hbox_next_turn_btn = QHBoxLayout()
        hbox_next_turn_btn.addStretch(0)
        hbox_next_turn_btn.addWidget(self.next_turn_btn)

        hbox_widg = QHBoxLayout()
        hbox_widg.addWidget(self.paint_widget)

        main_vbox = QVBoxLayout(self)
        main_vbox.addLayout(hbox_widg)
        main_vbox.addLayout(hbox_next_turn_btn)

        self.__layouts.append(main_vbox)
        self.__layouts.append(hbox_widg)
        self.__layouts.append(hbox_next_turn_btn)

        self.setLayout(main_vbox)

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
    train_color = QColor(25, 64, 255)

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

        points, vert_radius = self.calc_coordinates()

        h_painter = QPainter()
        h_painter.begin(self)

        self.draw_edges_and_waypoints(h_painter, points, vert_radius)
        self.draw_vertices(h_painter, points, vert_radius)
        self.draw_towns(h_painter, self.parent().parent().game.towns, points, vert_radius)
        self.draw_markets(h_painter, self.parent().parent().game.markets, points, vert_radius)
        self.draw_storages(h_painter, self.parent().parent().game.storages, points, vert_radius)
        self.draw_trains(h_painter, self.parent().parent().game.trains, points, vert_radius)

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

    def draw_edges_and_waypoints(self, h_painter, points, vert_radius):
        edge_pen = QPen(self.edge_color, self.edge_width, Qt.SolidLine)
        h_painter.setBrush(self.vertex_color)
        for vertex in self.__graph.get_all_vertices():
            for adj_vert in self.__graph.get_adj_vertices(vertex):
                h_painter.setPen(edge_pen)
                p1 = points[vertex]
                p2 = points[adj_vert]
                h_painter.drawLine(p1, p2)

                h_painter.setPen(self.vertex_pen)
                edge = self.__graph.get_edge_by_adj_vert(vertex, adj_vert)
                line = QLineF(p1, p2)
                for i in range(1, edge['length']):
                    cx = p1.x() + (i / edge['length']) * line.dx()
                    cy = p1.y() + (i / edge['length']) * line.dy()
                    h_painter.drawEllipse(cx - vert_radius/4, cy - vert_radius/4, vert_radius/2, vert_radius/2)

    def draw_vertices(self, h_painter, points, radius):
        h_painter.setFont(QFont('Decorative', 10))
        h_painter.setBrush(self.vertex_color)
        h_painter.setPen(self.vertex_pen)
        for vertex in self.__graph.get_all_vertices():
            x = points[vertex].x() - radius
            y = points[vertex].y() - radius
            h_painter.drawEllipse(x, y, 2 * radius, 2 * radius)

    def draw_towns(self, h_painter, towns, points, radius):
        for town in towns.values():
            if town.level == 1:
                pixmap = QPixmap("source\icons\\town_lvl1.png")
            elif town.level == 2:
                pixmap = QPixmap("source\icons\\town_lvl2.png")
            elif town.level == 3:
                pixmap = QPixmap("source\icons\\town_lvl3.png")
            x = points[town.point_idx].x() - radius
            y = points[town.point_idx].y() - radius
            h_painter.drawPixmap(QPointF(x, y), pixmap.scaled(2*radius, 2*radius, Qt.KeepAspectRatio))
            rect = QRectF(x + radius, y - 4*radius, 6*radius, 6*radius)
            h_painter.drawText(rect, Qt.AlignHCenter | Qt.AlignTop, '👤' + str(town.population) +
                               '\n🍽️{}/{}'.format(town.product, town.product_capacity) +
                               '\n⛉{} / {}'.format(town.armor, town.armor_capacity))

    def draw_markets(self, h_painter, markets, points, radius):
        pixmap = QPixmap("source\icons\market.png").scaled(2 * radius, 2 * radius, Qt.KeepAspectRatio)
        for market in markets.values():
            x = points[market.point_idx].x() - radius
            y = points[market.point_idx].y() - radius
            h_painter.drawPixmap(QPointF(x, y), pixmap.scaled(2*radius, 2*radius, Qt.KeepAspectRatio))
            rect = QRectF(x + radius, y - 3 * radius, 6 * radius, 6 * radius)
            h_painter.drawText(rect, Qt.AlignHCenter | Qt.AlignTop, '+' + str(market.replenishment) +
                               '\n🍽️{}/{}'.format(market.product, market.product_capacity))

    def draw_storages(self, h_painter, storages, points, radius):
        pixmap = QPixmap("source\icons\storage.png").scaled(2 * radius, 2 * radius, Qt.KeepAspectRatio)
        for storage in storages.values():
            x = points[storage.point_idx].x() - radius
            y = points[storage.point_idx].y() - radius
            h_painter.drawPixmap(QPointF(x, y), pixmap.scaled(2*radius, 2*radius, Qt.KeepAspectRatio))
            rect = QRectF(x + radius, y - 3 * radius, 6 * radius, 6 * radius)
            h_painter.drawText(rect, Qt.AlignHCenter | Qt.AlignTop, '+' + str(storage.replenishment) +
                               '\n⛉{}/{}'.format(storage.armor, storage.armor_capacity))

    def draw_trains(self, h_painter, trains, points, vert_radius):
        h_painter.setBrush(self.train_color)
        h_painter.setFont(QFont("Times", 7))
        for train in trains.values():
            self.draw_train(h_painter, train, points, vert_radius)

    def draw_train(self, h_painter, train, points, vert_radius):
        edge = self.__graph.get_edge_by_idx(train.line_idx)
        p1 = points[edge['vert_from']]
        p2 = points[edge['vert_to']]
        length = edge['length']
        line = QLineF(p1, p2)
        cx = p1.x() + (train.position/length)*line.dx()
        cy = p1.y() + (train.position/length)*line.dy()
        rect = QRectF(cx - vert_radius*2/3, cy - vert_radius*2/3, vert_radius*4/3, vert_radius*4/3)
        h_painter.setPen(Qt.black)
        h_painter.drawRect(rect)
        h_painter.setPen(Qt.white)
        h_painter.drawText(rect, Qt.AlignCenter, str(train.goods))
