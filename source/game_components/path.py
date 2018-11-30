class Path:
    def __init__(self):
        self.__vertices = [14, 20, 19, 13]
        self.__i = 0

    def next_vert(self):
        vert = self.__vertices[self.__i]
        self.__i += 1
        if self.__i == len(self.__vertices):
            self.__i = 0
        return vert
