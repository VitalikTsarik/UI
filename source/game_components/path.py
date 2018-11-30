class Path:
    def __init__(self, vertices):
        self.__vertices = vertices
        self.__i = 0

    def next_vert(self):
        vert = self.__vertices[self.__i]
        self.__i += 1
        if self.__i == len(self.__vertices):
            self.__i = 0
        return vert
