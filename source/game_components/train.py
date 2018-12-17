class Train:
    def __init__(self, idx, speed, level, next_level_price, line_idx, position, player_idx, events, goods,
                 goods_capacity, cooldown):
        self.__idx = idx
        self.__speed = speed
        self.__level = level
        self.__next_level_price = next_level_price
        self.__line_idx = line_idx
        self.__position = position
        self.__player_idx = player_idx
        self.__cooldown = cooldown
        self.__events = events
        # self.__fuel = fuel
        # self.__fuel_capacity = fuel_capacity
        # self.__fuel_consumption = fuel_consumption
        self.__goods = goods
        self.__goods_capacity = goods_capacity
        # self.__goods_type = goods_type

    @property
    def idx(self):
        return self.__idx

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        self.__speed = value

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value

    @property
    def next_level_price(self):
        return self.__next_level_price

    @next_level_price.setter
    def next_level_price(self, value):
        self.__next_level_price = value

    @property
    def line_idx(self):
        return self.__line_idx

    @line_idx.setter
    def line_idx(self, value):
        self.__line_idx = value

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def player_idx(self):
        return self.__player_idx

    @property
    def cooldown(self):
        return self.__cooldown

    @cooldown.setter
    def cooldown(self, value):
        self.__cooldown = value

    @property
    def events(self):
        return self.__events

    @property
    def fuel(self):
        return self.__fuel

    @property
    def fuel_capacity(self):
        return self.__fuel_capacity

    @property
    def fuel_consumption(self):
        return self.__fuel_consumption

    @property
    def goods(self):
        return self.__goods

    @property
    def goods_capacity(self):
        return self.__goods_capacity

    @goods_capacity.setter
    def goods_capacity(self, value):
        self.__goods_capacity = value

    @property
    def goods_type(self):
        return self.__goods_type
