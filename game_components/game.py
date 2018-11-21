from client import *
from json_converter import dict_to_graph, dict_to_trains, dict_to_posts


class Game:
    def __init__(self, window):
        self.__main_window = window
        self.__client = ServerConnection()
        self.__client.login_action('NeBoris')
        self.__map_graph = dict_to_graph(self.__client.map_action(Layer.Layer0)[1])
        layer1 = self.__client.map_action(Layer.Layer1)[1]
        self.__trains = dict_to_trains(layer1)
        self.__posts = dict_to_posts(layer1)

    def next_turn(self):
        for train in self.trains.values():
            train.position += train.speed
            road = self.map_graph.get_edge(train.line_idx)
            if train.position == 0 or train.position == road['length']:
                train.speed = 0

    def move_train(self, train_idx, line_idx, speed):
        res, msg = self.__client.move_action(train_idx, line_idx, speed)
        if res == Result.OKEY.value:
            self.__trains[train_idx].line_idx = line_idx
            self.__trains[train_idx].speed = speed

    @property
    def map_graph(self):
        return self.__map_graph

    @property
    def trains(self):
        return self.__trains

    @property
    def posts(self):
        return self.__posts
