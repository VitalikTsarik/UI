class Player:
    def __init__(self, idx, in_game, name, rating, town):
        self.__idx = idx
        self.__in_game = in_game
        self.__name = name
        self.__rating = rating
        self.__town = town

    @property
    def idx(self):
        return self.__idx

    @property
    def in_game(self):
        return self.__in_game

    @property
    def name(self):
        return self.__name

    @property
    def rating(self):
        return self.__rating

    @property
    def town(self):
        return self.__town
