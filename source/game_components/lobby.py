from enum import Enum


class GameState(Enum):
    INIT = 1
    RUN = 2
    FINISHED = 3


class Lobby:
    def __init__(self, name, num_players, num_turns, state):
        self.name = name
        self.num_players = num_players
        self.num_turns = num_turns
        self.state = state

