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
    def __init__(self, server, port):
        self.__socket = socket.socket()
        self.__socket.connect((server, port))

    def login_action(self, name):
        data = dumps({'name': name})
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

    def logout_action(self):
        self.__request(Action.LOGOUT)
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
        if res == 0:
            size = unpack('i', self.__socket.recv(4))[0]
            if size:
                data = b''
                while size > 128:
                    data += self.__socket.recv(128)
                    size -= 128
                data += self.__socket.recv(size)
                return loads(data.decode('UTF-8'))
        return res
