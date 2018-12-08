import heapq
from math import inf


class PathManager:
    def __init__(self):
        self.__lengths = {}
        self.__ancestors = {}

    def init_all_paths(self, graph, town_idx):
        self.__lengths, self.__ancestors = self.min_paths(graph, town_idx)

    def min_paths(self, graph, start):
        is_visited = {}
        paths = {}
        ancestors = {}
        for vertex in graph.get_all_vertices():
            is_visited[vertex] = False

        path_priority = [(0, start, -1)]
        while path_priority:
            min_path = heapq.heappop(path_priority)
            if not is_visited[min_path[1]]:
                is_visited[min_path[1]] = True
                paths[min_path[1]] = min_path[0]
                ancestors[min_path[1]] = min_path[2]
                for edge in graph.get_adj_edges(min_path[1]):
                    if not is_visited[edge['vert_to']]:
                        heapq.heappush(path_priority, (min_path[0] + edge['length'], edge['vert_to'], min_path[1]))

        return paths, ancestors

    def min_path_for_markets(self, graph, start, markets):
        is_visited = {}
        paths = {}
        ancestors = {}
        for vertex in graph.get_all_vertices():
            is_visited[vertex] = False

        path_priority = [(0, start, -1)]
        while path_priority:
            min_path = heapq.heappop(path_priority)
            if not is_visited[min_path[1]]:
                is_visited[min_path[1]] = True
                paths[min_path[1]] = min_path[0]
                ancestors[min_path[1]] = min_path[2]
                for edge in graph.get_adj_edges(min_path[1]):
                    if not is_visited[edge['vert_to']]:
                        heapq.heappush(path_priority, (min_path[0] + edge['length'], edge['vert_to'], min_path[1]))

        return paths, ancestors



    def find_best_path(self, town, markets, train_capacity):
        idx = self.find_best_market(town, markets, train_capacity)
        path = []

        while idx != -1:
            path.append(idx)
            idx = self.__ancestors[idx]

        return path[-2::-1] + path[1:]

    def find_best_market(self, town, markets, train_capacity):
        best_market = -1
        max_goods = -inf
        min_len = inf
        min_people_died = inf

        for market in markets.values():
            if self.__count_died_people(town, 2*self.__length[market.point_idx]) <= min_people_died:
                from_market = min(train_capacity, market.product_capacity, market.product + market.replenishment * self.__length[market.point_idx])
                if from_market > max_goods or (from_market == max_goods and min_len > self.__length[market.point_idx]):
                    max_goods = from_market
                    best_market = market.point_idx
                    min_len = self.__lengths[market.point_idx]

        return best_market

    def __count_died_people(self, town, turns):
        product = town.product
        population = town.population
        while product >= 0:
            if turns == 0:
                return 0
            product -= population
            turns -= 1
        return turns

