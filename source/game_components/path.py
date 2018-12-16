class Path:
    def __init__(self, path, wait_before=0, wait_after=0):
        self.__i = -wait_before
        self.__path = path
        self.__wait_before = wait_before
        self.wait_after = wait_after

    def next_vert(self):
        if len(self.__path) > self.__i >= 0:
            next_vert = self.__path[self.__i]
        else:
            next_vert = None
        self.__i += 1
        return next_vert

    def has_next_vert(self):
        return self.__i < len(self.__path) + self.wait_after

    def concatenate(self, path):
        self.__path += path.path

    def add_vert(self, vert):
        self.__path.append(vert)

