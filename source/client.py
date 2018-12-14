# -*- coding: utf-8 -*-
import socket
from enum import Enum
from json import dumps, loads
from struct import pack, unpack
import time

SERVER = 'wgforge-srv.wargaming.net'
PORT = 443


class Action(Enum):
    LOGIN = 1
    LOGOUT = 2
    MOVE = 3
    UPGRADE = 4
    TURN = 5
    PLAYER = 6
    GAMES = 7
    MAP = 10


class Result(Enum):
    OKEY = 0
    BAD_COMMAND = 1
    RESOURCE_NOT_FOUND = 2
    ACCESS_DENIED = 3
    NOT_READY = 4
    TIMEOUT = 5
    INTERNAL_SERVER_ERROR = 500


class Layer(Enum):
    Layer0 = 0
    Layer1 = 1
    Layer10 = 10


class ServerConnection:
    def __init__(self, server=SERVER, port=PORT):
        self.__socket = socket.socket()
        self.__socket.settimeout(10)
        self.__socket.connect((server, port))

    def login_action(self, name, game, num_players=1, num_turns=-1):
        data = dumps({'name': name, 'game': game, 'num_players': num_players, 'num_turns': num_turns})
        self.__request(Action.LOGIN, data)
        return self.__response()

    def player_action(self):
        self.__request(Action.PLAYER)
        return self.__response()

    def map_action(self, layer):
        data = dumps({'layer': layer.value})
        self.__request(Action.MAP, data)
        return self.__response()

    def move_action(self, train_idx, line_idx, speed):
        data = dumps({"line_idx": line_idx, "speed": speed, "train_idx": train_idx})
        self.__request(Action.MOVE, data)
        return self.__response()

    def turn_action(self):
        self.__request(Action.TURN)
        return self.__response()

    def upgrade_action(self, posts_idxs, trains_idxs):
        data = dumps({"posts": posts_idxs, "trains": trains_idxs})
        self.__request(Action.UPGRADE, data)
        return self.__response()

    def logout_action(self):
        self.__request(Action.LOGOUT)
        return self.__response()

    def games_action(self):
        self.__request(Action.GAMES)
        return self.__response()

    def close(self):
        self.__socket.close()
        return self.__response()

    def __request(self, action, data=None):
        if data:
            msg = pack('ii', action.value, len(data)) + data.encode('UTF-8')
        else:
            msg = pack('ii', action.value, 0)
        self.__socket.send(msg)

    def __response(self):
        res = unpack('i', self.__socket.recv(4))[0]
        size = unpack('i', self.__socket.recv(4))[0]
        if size:
            data = b''
            while size > 4:
                data += self.__socket.recv(4)
                size -= 4
            data += self.__socket.recv(size)
            if res != Result.OKEY.value:
                raise ConnectionError('res: {}, mag: {}'.format(res, data))
            return loads(data.decode('UTF-8'))
        if res != Result.OKEY.value:
            raise ConnectionError('res: {}'.format(res))
        return 0


if __name__ == '__main__':
    cnt = ServerConnection()
    g = cnt.games_action()
    print(g)
