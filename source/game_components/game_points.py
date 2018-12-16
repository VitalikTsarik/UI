class GamePoint:
    def __init__(self, idx, name, point_idx):
        self.__idx = idx
        self.__name = name
        self.__point_idx = point_idx
        # self.__events = events

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
    def __init__(self, idx, name, point_idx, armor, armor_capacity, level,
                 population, population_capacity, product, product_capacity, player_idx):
        super().__init__(idx, name, point_idx)
        self.__armor = armor
        self.__armor_capacity = armor_capacity
        self.__level = level
        self.__population = population
        self.__population_capacity = population_capacity
        self.__product = product
        self.__product_capacity = product_capacity
        self.__player_idx = player_idx
        # self.__train_cooldown = train_cooldown

    @property
    def armor(self):
        return self.__armor

    @armor.setter
    def armor(self, value):
        self.__armor = value

    @property
    def armor_capacity(self):
        return self.__armor_capacity

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value

    @property
    def population(self):
        return self.__population

    @property
    def population_capacity(self):
        return self.__product_capacity

    @property
    def product(self):
        return self.__product

    @product.setter
    def product(self, value):
        self.__product = value

    @property
    def product_capacity(self):
        return self.__product_capacity

    @property
    def train_cooldown(self):
        return self.__train_cooldown

    @property
    def player_idx(self):
        return self.__player_idx


class Market(GamePoint):
    def __init__(self, idx, name, point_idx, product, product_capacity, replenishment):
        super().__init__(idx, name, point_idx)
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
    def __init__(self, idx, name, point_idx, armor, armor_capacity, replenishment):
        super().__init__(idx, name, point_idx)
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
