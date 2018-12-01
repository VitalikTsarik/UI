from source.client import *
from source.json_converter import dict_to_graph, dict_to_trains, dict_to_posts
from source.game_components.path import Path


class Game:
    def __init__(self):
        self.__client = ServerConnection()
        self.__client.login_action('NeBoris')
        self.__map_graph = dict_to_graph(self.__client.map_action(Layer.Layer0)[1])
        layer1 = self.__client.map_action(Layer.Layer1)[1]
        self.__trains = dict_to_trains(layer1)
        self.__town, self.__markets, self.__storages = dict_to_posts(layer1)
        self.__path = Path()
        self.set_direction(self.__path.next_vert())

    def next_turn(self):
        if self.town.product < self.town.population:
            return -1
        self.town.product -= self.town.population
        for train in self.__trains.values():  # todo: добавить загрузку продуктов в поезд из маркета и выгрузку в город
            train.position += train.speed
            road = self.__map_graph.get_edge_by_idx(train.line_idx)

            if train.position == 0 or train.position == road['length']:
                if train.speed != 0:
                    train.speed = 0
                    self.set_direction(self.__path.next_vert())
        return 0

    def move_train(self, train_idx, line_idx, speed):
        res, msg = self.__client.move_action(train_idx, line_idx, speed)
        if res == Result.OKEY.value:
            self.__trains[train_idx].line_idx = line_idx
            self.__trains[train_idx].speed = speed

    def set_direction(self, next_vert_idx):
        train_idx = 1  # временно

        if self.__trains[train_idx].position == 0:
            curr_vert = self.__map_graph.get_edge_by_idx(self.__trains[train_idx].line_idx)['vert_from']
        else:
            curr_vert = self.__map_graph.get_edge_by_idx(self.__trains[train_idx].line_idx)['vert_to']

        new_line = self.__map_graph.get_edge_by_adj_vert(next_vert_idx, curr_vert)
        if curr_vert == new_line['vert_from']:
            self.__trains[train_idx].position = 0
            self.move_train(train_idx, new_line['edge_idx'], 1)
        else:
            self.__trains[train_idx].position = new_line['length']
            self.move_train(train_idx, new_line['edge_idx'], -1)

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

    @property
    def map_graph(self):
        return self.__map_graph

    @property
    def trains(self):
        return self.__trains

    @property
    def town(self):
        return self.__town

    @property
    def markets(self):
        return self.__markets

    @property
    def storages(self):
        return self.__storages