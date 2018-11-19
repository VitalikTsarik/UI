class Train:
    def __init__(self, idx, speed, level, line_idx, position, player_idx):
        self.__idx = idx
        self.__speed = speed
        self.__level = level

        self.__line_idx = line_idx
        self.__position = position

        self.__player_idx = player_idx

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

    @property
    def player_idx(self):
        return self.__player_idx

    @line_idx.setter
    def line_idx(self, value):
        self.__line_idx = value

    @position.setter
    def position(self, value):
        self.__position = value
