from client import *
from json_converter import dict_to_graph, dict_to_trains, dict_to_posts


class Game:
    def __init__(self):
        self.__client = ServerConnection()
        self.__client.login_action('NeBoris')
        self.__map_graph = dict_to_graph(self.__client.map_action(Layer.Layer0)[1])
        layer1 = self.__client.map_action(Layer.Layer1)[1]
        self.__trains = dict_to_trains(layer1)
        self.__init_trains_start_idx_()
        self.__posts = dict_to_posts(layer1)
       # self.set_direction(self.__trains[1].start_vert)

    def __init_trains_start_idx_(self):
        for train in self.__trains.values():
            train.start_vert = self.__map_graph.get_edge_by_idx(train.line_idx)['vert_from']

    def next_turn(self):
        for train in self.__trains.values():
            train.position += train.speed
            road = self.__map_graph.get_edge_by_idx(train.line_idx)

            if train.position == 0 and train.speed != 0:
                train.speed = 0
                if train.start_vert == road['vert_from']:
                    cur_vert_idx = road['vert_from']
                else:
                    cur_vert_idx = road['vert_to']
            elif train.position == road['length'] and train.speed != 0:
                train.speed = 0
                if train.start_vert == road['vert_from']:
                    cur_vert_idx = road['vert_to']
                else:
                    cur_vert_idx = road['vert_from']
            else:
                return -1
            train.start_vert = cur_vert_idx
            train.position = 0
            return cur_vert_idx

    def move_train(self, train_idx, line_idx, speed):
        res, msg = self.__client.move_action(train_idx, line_idx, speed)
        if res == Result.OKEY.value:
            self.__trains[train_idx].line_idx = line_idx
            self.__trains[train_idx].speed = speed
        a =0

    def set_direction(self, next_vert_idx):
        train_idx = 1 # временно
        new_line = self.__map_graph.get_edge_by_adj_vert(next_vert_idx, self.trains[train_idx].start_vert)
        self.move_train(train_idx, new_line['edge_idx'], 1)

    def move_forward(self):
        train_idx = 1 # временно
        train = self.trains[train_idx]
        self.move_train(train.idx, train.line_idx, 1)

    def stop_train(self):
        train_idx = 1 # временно
        train = self.trains[train_idx]
        self.move_train(train.idx, train.line_idx, 0)

    def move_backwards(self):
        train_idx = 1 # временно
        train = self.trains[train_idx]
        self.move_train(train.idx, train.line_idx, -1)

    @property
    def map_graph(self):
        return self.__map_graph

    @property
    def trains(self):
        return self.__trains

    @property
    def posts(self):
        return self.__posts
