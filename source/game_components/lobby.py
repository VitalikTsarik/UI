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
        if state == GameState.INIT.value:
            self.state = 'init'
        elif state == GameState.RUN.value:
            self.state = 'run'
        elif state == GameState.FINISHED.value:
            self.state = 'finished'
