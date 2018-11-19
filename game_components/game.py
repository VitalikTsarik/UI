from Client import *
from json_converter import dict_to_graph


class Game:
    def __init__(self, window):
        self.__main_window = window
        self.__client = ServerConnection()
        self.__client.login_action('NeBoris')
        self.__map_graph = dict_to_graph(self.__client.map_action(Layer.Layer0))
        # todo: parse from Layer1 to trains and posts
        layer1 = self.__client.map_action(Layer.Layer1)
        self.__posts = []
        self.__trains = []

    @property
    def map_graph(self):
        return self.__map_graph

    @property
    def trains(self):
        return self.__trains

    @property
    def posts(self):
        return self.__posts
