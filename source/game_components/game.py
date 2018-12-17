from client import *
from json_converter import dict_to_graph, dict_to_trains, dict_to_posts, dict_to_player, dict_to_lobbies
from game_components.path_manager import PathManager

EMERGENCY_ARMOR_RESERVE = 25
TRAINS_TO_MARKETS = 6/8
TRAINS_TO_STORAGES = 1 - TRAINS_TO_MARKETS


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
        self.__paths = {}
        self.__paths_to_market = {}
        self.__paths_to_storage = {}
        self.__trains_to_market = {}
        self.__trains_to_storage = {}
        self.__stopped_trains_direction = {}
        self.__trains_to_market_lvl = 0
        self.__trains_to_storage_lvl = 0

    def start_game(self):
        self.__path_manager.init_all_paths(self.__map_graph, self.player.town.point_idx,
                                           self.__markets, self.__storages)

        for train in self.__trains_to_market.values():
            self.__trains_to_market_lvl += train.level
        for train in self.__trains_to_storage.values():
            self.__trains_to_storage_lvl += train.level

        self.next_turn()

    def next_turn(self):
        self.update_layer1()
        self.update_player()

        if self.all_trains_in_group_in_town(self.__trains_to_market):
            self.update_trains_if_possible(self.__trains_to_market)
            self.__paths_to_market = self.__path_manager.paths_to_market(self.__map_graph, self.player.town,
                                                                         self.__markets, self.__trains_to_market)
        for train in self.__trains_to_market.values():
            road = self.__map_graph.get_edge_by_idx(train.line_idx)
            if train.position == 0 or train.position == road['length']:
                if self.__paths_to_market[train.idx].has_next_vert():
                    next_vert = self.__paths_to_market[train.idx].next_vert()
                    if next_vert is None:
                        continue
                    else:
                        self.set_direction(train, next_vert)
            else:
                if self.collision_can_happened(train):
                    self.stop_train(train)
                else:
                    self.move_forward(train)

        if self.all_trains_in_group_in_town(self.__trains_to_storage):
            self.upgrade_post_if_possible(self.player.town)
            self.update_trains_if_possible(self.__trains_to_storage)
            self.__paths_to_storage = self.__path_manager.paths_to_storage(self.__map_graph, self.player.town,
                                                                           self.__storages, self.__trains_to_storage)
        for train in self.__trains_to_storage.values():
            road = self.__map_graph.get_edge_by_idx(train.line_idx)
            if train.position == 0 or train.position == road['length']:
                if self.__paths_to_storage[train.idx].has_next_vert():
                    next_vert = self.__paths_to_storage[train.idx].next_vert()
                    if next_vert is None:
                        continue
                    else:
                        self.set_direction(train, next_vert)
            else:
                if self.collision_can_happened(train):
                    self.stop_train(train)
                else:
                    self.move_forward(train)

    def update_layer1(self):
        layer1 = self.__client.map_action(Layer.Layer1)
        self.__trains = dict_to_trains(layer1)
        for train in self.__trains.values():
            if train.player_idx == self.player.idx:
                self.__player_trains[train.idx] = train

        n = len(self.__player_trains)
        i = 0
        for train in self.__player_trains.values():
            if train.player_idx == self.player.idx:
                if i < n*TRAINS_TO_MARKETS:
                    self.__trains_to_market[train.idx] = train
                else:
                    self.__trains_to_storage[train.idx] = train
                i += 1
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

    def collision_can_happened(self, train):
        line = self.map_graph.get_edge_by_idx(train.line_idx)
        if line['vert_from'] == self.player.town.point_idx and train.position == 1 and train.speed == -1:
            return False
        if line['vert_to'] == self.player.town.point_idx and train.position == line['length'] - 1 and train.speed == 1:
            return False

        for another_train in self.__trains.values():
            if train.line_idx == another_train.line_idx and another_train.speed == 0:
                if train.idx in self.__stopped_trains_direction.keys():
                    speed = self.__stopped_trains_direction[train.idx]
                else:
                    speed = train.speed
                if speed == 1 and another_train.position == train.position + 1 or \
                        speed == -1 and another_train.position == train.position - 1:
                    return True
        return False

    def move_forward(self, train):
        if train.speed == 0:
            speed = self.__stopped_trains_direction.pop(train.idx)
            self.move_train(train.idx, train.line_idx, speed)

    def stop_train(self, train):
        if train.speed != 0:
            self.__stopped_trains_direction[train.idx] = train.speed
            self.move_train(train.idx, train.line_idx, 0)

    def move_backwards(self):
        train_idx = 1  # временно
        train = self.trains[train_idx]
        self.move_train(train.idx, train.line_idx, -1)

    def next_turn_action(self):
        self.__client.turn_action()

    def update_trains_if_possible(self, trains):
        if trains.keys() == self.__trains_to_market.keys():
            for train in self.__trains_to_market.values():
                self.upgrade_train_if_possible(train)
                self.__trains_to_market_lvl += 1
                if self.__trains_to_market_lvl*TRAINS_TO_MARKETS <= self.__trains_to_storage_lvl*TRAINS_TO_STORAGES:
                    break
        else:
            for train in self.__trains_to_storage.values():
                self.upgrade_train_if_possible(train)
                self.__trains_to_storage_lvl += 1
                if self.__trains_to_storage_lvl*TRAINS_TO_STORAGES < self.__trains_to_market_lvl*TRAINS_TO_MARKETS:
                    break

    def upgrade_train_if_possible(self, train):
        if train.next_level_price:
            if self.player.town.armor >= train.next_level_price + EMERGENCY_ARMOR_RESERVE:
                self.__client.upgrade_action([], [train.idx])
                self.player.town.armor -= train.next_level_price
                train.level += 1
                train.next_level_price *= 2
                train.goods_capacity *= 2

    def upgrade_post_if_possible(self, post):
        if post.next_level_price:
            if self.player.town.armor >= post.next_level_price + EMERGENCY_ARMOR_RESERVE:
                self.__client.upgrade_action([post.idx], [])
                self.player.town.armor -= post.next_level_price
                post.level += 1
                post.next_level_price *= 2

    def all_trains_in_group_in_town(self, group):
        lines = self.__map_graph.get_adj_edges(self.player.town.point_idx)

        for train in group.values():
            town_line = None
            for line in lines:
                if train.line_idx == line['edge_idx']:
                    town_line = line
                    break
            if town_line is None:
                return False
            if town_line['start_vert'] == self.player.town.point_idx:
                if train.position != 0:
                    return False
            else:
                if train.position != town_line['length']:
                    return False
        return True

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
