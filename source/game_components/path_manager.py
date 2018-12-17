import heapq
from math import inf
from game_components.path import Path


class PathManager:
    def __init__(self):
        self.__lengths = {}
        self.__ancestors = {}
        self.__lengths_markets = {}
        self.__ancestors_markets = {}
        self.__lengths_storage = {}
        self.__ancestors_storage = {}
        self.__ignored_vertices_to_market = []
        self.__ignored_vertices_to_storage = []

    def init_all_paths(self, graph, town_idx, markets, storage):
        self.__lengths, self.__ancestors = self.min_paths(graph, town_idx, None)
        self.__lengths_markets, self.__ancestors_markets = self.min_paths(graph, town_idx, markets.keys())
        self.__lengths_storage, self.__ancestors_storage = self.min_paths(graph, town_idx, storage.keys())

    def min_paths(self, graph, start, posts_to_find, ignored_vertices=None):
        is_visited = {}
        paths = {}
        ancestors = {}

        if posts_to_find:
            for vertex in graph.get_all_vertices():
                post_idx = graph.get_post_idx(vertex)
                if not post_idx or vertex == start or post_idx in posts_to_find:
                    is_visited[vertex] = False
                else:
                    is_visited[vertex] = True
        else:
            for vertex in graph.get_all_vertices():
                is_visited[vertex] = False

        if ignored_vertices:
            for vertex in ignored_vertices:
                is_visited[vertex] = True

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

    def paths_to_market(self, graph, town, markets, train_group):
        lengths, ancestors = self.min_paths(graph, town.point_idx, markets, self.__ignored_vertices_to_market)
        market_idx = self.find_best_market(town, markets, sum([train.goods_capacity for train in train_group.values()]))
        path_to = []
        path_from = []

        idx = market_idx
        while idx != -1:
            path_to.append(idx)
            idx = ancestors[idx]

        lengths, ancestors = self.min_paths(graph, market_idx, None, [path_to[1]] + self.__ignored_vertices_to_market)
        idx = town.point_idx
        while idx != -1:
            path_from.append(idx)
            idx = ancestors[idx]

        self.__ignored_vertices_to_storage = path_to[:-1] + path_from[1:]

        paths = {}

        market = markets[graph.get_post_idx(market_idx)]
        i = 0
        for train in train_group.values():
            paths[train.idx] = Path(path_to[-2::-1] + path_from[-2::-1], i)
            path = path_to[-2::-1]
            wait_beside = (train.goods_capacity - market.product) // market.replenishment
            market.product -= train.goods_capacity
            if market.product < 0:
                market.product = 0
            path += [None for i in range(wait_beside)]
            path += path_from[-2::-1]
            paths[train.idx] = Path(path, i)
            i += 1
        return paths

    def paths_to_storage(self, graph, town, storages, train_group):
        lengths, ancestors = self.min_paths(graph, town.point_idx, storages, self.__ignored_vertices_to_storage)
        storage_idx = self.find_best_storage(town, storages, sum([train.goods_capacity for train in train_group.values()]))
        path_to = []
        path_from = []

        idx = storage_idx
        while idx != -1:
            path_to.append(idx)
            idx = ancestors[idx]

        lengths, ancestors = self.min_paths(graph, storage_idx, None, [path_to[1]] + self.__ignored_vertices_to_storage)
        idx = town.point_idx
        while idx != -1:
            path_from.append(idx)
            idx = ancestors[idx]

        self.__ignored_vertices_to_market = path_to[:-1] + path_from[1:]

        paths = {}

        storage = storages[graph.get_post_idx(storage_idx)]
        i = 0
        for train in train_group.values():
            path = path_to[-2::-1]
            wait_beside = (train.goods_capacity - storage.armor)//storage.replenishment - \
                          (1 if storage.armor != storage.armor_capacity else 0)
            storage.armor -= train.goods_capacity
            if storage.armor < 0:
                storage.armor = 0
            path += [None for i in range(wait_beside)]
            path += path_from[-2::-1]
            paths[train.idx] = Path(path, i)
            i += 1
        return paths

    def find_best_market(self, town, markets, train_capacity):
        best_market = -1
        max_goods = -inf
        min_len = inf

        for market in markets.values():
                from_market = min(train_capacity, market.product_capacity, market.product + market.replenishment * self.__lengths_markets[market.point_idx])
                if from_market > max_goods or (from_market == max_goods and min_len > self.__lengths_markets[market.point_idx] + self.__lengths[market.point_idx]):
                    max_goods = from_market
                    best_market = market.point_idx
                    min_len = self.__lengths_markets[market.point_idx] + self.__lengths[market.point_idx]
        return best_market

    def find_best_storage(self, town, storages, train_capacity):
        best_storage = -1
        max_goods = -inf
        min_len = inf

        for storage in storages.values():
                from_storage = min(train_capacity, storage.armor_capacity, storage.armor + storage.replenishment * self.__lengths_storage[storage.point_idx])
                if from_storage > max_goods or (from_storage == max_goods and min_len > self.__lengths_storage[storage.point_idx] + self.__lengths[storage.point_idx]):
                    max_goods = from_storage
                    best_storage = storage.point_idx
                    min_len = self.__lengths_storage[storage.point_idx] + self.__lengths[storage.point_idx]
        return best_storage
