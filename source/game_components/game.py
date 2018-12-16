from source.client import *
from source.json_converter import dict_to_graph, dict_to_trains, dict_to_posts, dict_to_player, dict_to_lobbies
from source.game_components.path_manager import PathManager


class Game:
    def __init__(self):
        self.__client = ServerConnection()
        self.__lobby = None
        self.__path_manager = PathManager()
        self.player = None
        self.__map_graph = None
        self.__trains = {}
        self.__player_trains = {}
        self.__towns = {}
        self.__markets = {}
        self.__storages = {}
        self.__path = None

    def start_game(self):
        self.__path_manager.init_all_paths(self.__map_graph, self.player.town.point_idx,
                                           self.__markets, self.__storages)
        for train in self.__player_trains.values():
            self.upgrade_train_if_possible(train)
        self.upgrade_post_if_possible(self.player.town)
        self.__path = self.__path_manager.find_best_path(self.player.town, self.markets, self.storages,
                                                         self.trains[1].goods_capacity)
        self.set_direction(self.__player_trains[1], self.__path.next())

    def next_turn(self):
        self.update_layer1()
        self.update_player()
        train = self.__player_trains[1]  # todo: сделать цикл для всех поездов !!!
        road = self.__map_graph.get_edge_by_idx(train.line_idx)
        if train.position == 0 or train.position == road['length']:
            if self.__path.has_next():
                self.set_direction(train, self.__path.next())
            else:
                self.upgrade_train_if_possible(train)
                self.upgrade_post_if_possible(self.player.town)
                self.__path = self.__path_manager.find_best_path(self.player.town, self.markets, self.storages,
                                                                 self.trains[1].goods_capacity)

    def update_layer1(self):
        layer1 = self.__client.map_action(Layer.Layer1)
        self.__trains = dict_to_trains(layer1)
        for train in self.__trains.values():
            if train.player_idx == self.player.idx:
                self.__player_trains[train.idx] = train
        self.__towns, self.__markets, self.__storages = dict_to_posts(layer1)

    def update_player(self):
        self.player = dict_to_player(self.__client.player_action())

    def move_train(self, train_idx, line_idx, speed):
        self.__client.move_action(train_idx, line_idx, speed)
        self.__trains[train_idx].line_idx = line_idx
        self.__trains[train_idx].speed = speed

    def set_direction(self, train, next_vert_idx):

        if train.position == 0:
            curr_vert = self.__map_graph.get_edge_by_idx(train.line_idx)['vert_from']
        else:
            curr_vert = self.__map_graph.get_edge_by_idx(train.line_idx)['vert_to']

        new_line = self.__map_graph.get_edge_by_adj_vert(next_vert_idx, curr_vert)
        if curr_vert == new_line['vert_from']:
            train.position = 0
            self.move_train(train.idx, new_line['edge_idx'], 1)
        else:
            train.position = new_line['length']
            self.move_train(train.idx, new_line['edge_idx'], -1)

    def move_forward(self):
        train_idx = 1  # временно
        train = self.trains[train_idx]
        self.move_train(train.idx, train.line_idx, 1)

    def stop_train(self):
        train_idx = 1  # временно
        train = self.trains[train_idx]
        self.move_train(train.idx, train.line_idx, 0)

    def move_backwards(self):
        train_idx = 1  # временно
        train = self.trains[train_idx]
        self.move_train(train.idx, train.line_idx, -1)

    def next_turn_action(self):
        self.__client.turn_action()

    def upgrade_train_if_possible(self, train):
        if train.level == 1 and self.player.town.armor >= 40:
            self.__client.upgrade_action([], [train.idx])
            self.player.town.armor -= 40
            train.level = 2
        if train.level == 2 and self.player.town.armor >= 80:
            self.__client.upgrade_action([], [train.idx])
            self.player.town.armor -= 80
            train.level = 3

    def upgrade_post_if_possible(self, post):
        if post.level == 1 and self.player.town.armor >= 100:
            self.__client.upgrade_action([post.idx], [])
            self.player.town.armor -= 100
            post.level = 2
        if post.level == 2 and self.player.town.armor >= 200:
            self.__client.upgrade_action([post.idx], [])
            self.player.town.armor -= 200
            post.level = 3

    def new_game(self, player_name, lobby):
        if self.player is not None:
            self.__client.logout_action()
            self.__client = ServerConnection()
        self.__lobby = lobby
        self.player = dict_to_player(self.__client.login_action(player_name, lobby.name, lobby.num_players, lobby.num_turns))
        self.__map_graph = dict_to_graph(self.__client.map_action(Layer.Layer0))
        self.update_layer1()
        self.update_player()

    def connect_to_game(self, player_name, lobby):
        if self.player is not None:
            self.__client.logout_action()
            self.__client = ServerConnection()
        self.__lobby = lobby
        self.player = dict_to_player(self.__client.connect_to_game(player_name, lobby.name))
        self.__map_graph = dict_to_graph(self.__client.map_action(Layer.Layer0))
        self.update_layer1()
        self.update_player()

    def get_existing_games(self):
        return dict_to_lobbies(self.__client.games_action())

    @property
    def map_graph(self):
        return self.__map_graph

    @property
    def trains(self):
        return self.__trains

    @property
    def towns(self):
        return self.__towns

    @property
    def markets(self):
        return self.__markets

    @property
    def storages(self):
        return self.__storages

    @property
    def lobby(self):
        return self.__lobby

    @lobby.setter
    def lobby(self, value):
        self.__lobby = value
