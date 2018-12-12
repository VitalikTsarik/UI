class Path:
    def __init__(self, path, length):
        self.__i = 0
        self.__path = path
        self.__length = length

    def next(self):
        next_vert = self.__path[self.__i]
        self.__i += 1
        return next_vert

    def has_next(self):
        return self.__i < len(self.__path)

    def concatenate(self, path):
        self.__path += path

    def add_vert(self, vert):
        self.__path.append(vert)

    @property
    def length(self):
        return self.__length
