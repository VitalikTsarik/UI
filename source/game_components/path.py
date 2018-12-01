class Path:
    def __init__(self):
        self.__calc_path()

    def __calc_path(self):
        self.__vertices = [14, 20, 19, 13]  # todo: вставить алгоритм просчёта пути
        self.__i = 0

    def next_vert(self):
        if self.__i == len(self.__vertices):
            self.__calc_path()
        vert = self.__vertices[self.__i]
        self.__i += 1
        return vert
