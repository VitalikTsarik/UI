class Train:
    def __init__(self, idx, speed):
        self.__idx = idx
        self.__speed = speed

    @property
    def idx(self):
        return self.__idx

    @property
    def speed(self):
        return self.__speed


class GamePoint:
    def __init__(self, idx):
        self.__idx = idx

    @property
    def idx(self):
        return self.__idx


class Town(GamePoint):
    def __init__(self, idx):
        super().__init__(idx)


class Market(GamePoint):
    def __init__(self, idx):
        super().__init__(idx)


class Storage(GamePoint):
    def __init__(self, idx):
        super().__init__(idx)
