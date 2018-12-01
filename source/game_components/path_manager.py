import heapq
from math import inf


class PathManager:
    def __init__(self):
        self.__length = {}
        self.__ancestors = {}
        # self.__markets_lengths = {}

    def init_all_paths(self, graph, town_idx):
        self.__length, self.__ancestors = self.min_paths_from_town(graph, town_idx)

    # def init_market_lengths(self, graph):
    #     for vertex in graph.get_post_vertices():
    #         self.__markets_lengths[vertex] = self.__length[vertex]

    def min_paths_from_town(self, graph, start):
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
            idx = self.__length[idx]

        return path

    def find_best_market(self, town, markets, train_capacity):
        best_market = -1
        max_goods = -inf
        min_len = inf

        for idx, market in markets:
            if 2 * self.__length[idx] * town.population >= town.product:
                from_market = min(train_capacity, market.product_capacity, market.product + market.replenishment * self.__length[idx])
                if from_market > max_goods or (from_market == max_goods and min_len > self.__length[idx]) :
                    max_goods = from_market
                    best_market = idx
                    min_len = self.__length[idx]

        return best_market
