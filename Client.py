# -*- coding: utf-8 -*-
from enum import Enum

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
