class Train:
    def __init__(self, idx, speed, level, line_idx, position, player_idx, cooldown, events, fuel, fuel_capacity,
                 fuel_consumption, goods, goods_capacity, goods_type):
        self.__idx = idx
        self.__speed = speed
        self.__level = level
        self.__line_idx = line_idx
        self.__position = position
        self.__player_idx = player_idx
        self.__cooldown = cooldown
        self.__events = events
        self.__fuel = fuel
        self.__fuel_capacity = fuel_capacity
        self.__fuel_consumption = fuel_consumption
        self.__goods = goods
        self.__goods_capacity = goods_capacity
        self.__goods_type = goods_type

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

    @property
    def goods_type(self):
        return self.__goods_type

class GamePoint:
    def __init__(self, idx, name, point_idx, events):
        self.__idx = idx
        self.__name = name
        self.__point_idx = point_idx
        self.__events = events

    @property
    def idx(self):
        return self.__idx

    @property
    def name(self):
        return self.__name

    @property
    def point_idx(self):
        return self.__point_idx

    @property
    def events(self):
        return self.__events


class Town(GamePoint):
    def __init__(self, idx, name, point_idx, events, armor, armor_capacity, level,
                 population, population_capacity, product, product_capacity, train_cooldown):
        super().__init__(idx, name, point_idx, events)
        self.__armor = armor
        self.__armor_capacity = armor_capacity
        self.__level = level
        self.__population = population
        self.__population_capacity = population_capacity
        self.__product = product
        self.__product_capacity = product_capacity
        self.__train_cooldown = train_cooldown

    @property
    def armor(self):
        return self.__armor

    @property
    def armor_capacity(self):
        return self.__armor_capacity

    @property
    def level(self):
        return self.__armor

    @property
    def population(self):
        return self.__population

    @property
    def population_capacity(self):
        return self.__product_capacity

    @property
    def product(self):
        return self.__product

    @property
    def product_capacity(self):
        return self.__product_capacity

    @property
    def train_cooldown(self):
        return self.__train_cooldown

class Market(GamePoint):
    def __init__(self, idx, name, point_idx, events, product, product_capacity, replenishment):
        super().__init__(idx, name, point_idx, events)
        self.__product = product
        self.__product_capacity = product_capacity
        self.__replenishment = replenishment

    @property
    def product(self):
        return self.__product

    @property
    def product_capacity(self):
        return self.__product_capacity

    @property
    def replenishment(self):
        return self.__replenishment


class Storage(GamePoint):
    def __init__(self, idx, name, point_idx, events, armor, armor_capacity, replenishment):
        super().__init__(idx, name, point_idx, events)
        self.__armor = armor
        self.__armor_capacity = armor_capacity
        self.__replenishment = replenishment

    @property
    def armor(self):
        return self.__armor

    @property
    def armor_capacity(self):
        return self.__armor_capacity

    @property
    def replenishment(self):
        return self.__replenishment