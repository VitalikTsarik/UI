class Train:
    def __init__(self, idx, speed, level, line_idx, position):
        self.__idx = idx
        self.__speed = speed
        self.__level = level

        self.__line_idx = line_idx
        self.__position = position


    @property
    def idx(self):
        return self.__idx

    @property
    def speed(self):
        return self.__speed

    @property
    def level(self):
        return self.__level

    @property
    def line_idx(self):
        return self.__line_idx

    @property
    def position(self):
        return self.__position

    @line_idx.setter
    def line_idx(self, value):
        self.__line_idx = value

    @position.setter
    def position(self, value):
        self.__position = value



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
