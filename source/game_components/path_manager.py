import heapq

if __name__ == '__main__':
    H = [(21, 'fofo', False),(1,'hoho'),(45, 'a'),(78, 'd'),(3, 'j'),(5, 'j')]
    # Covert to a heap
    heapq.heapify(H)
    print(H)
    # Add element
    heapq.heappush(H,(2, 'sdf'))
    print(H)
    min = heapq.heappop(H)
    print(min)
    print(H)


class PathManager:
    def __init__(self, graph, town_idx):
        self.__paths = {}
        self.dijkstra(graph, town_idx)

    def dijkstra(self, graph, town_idx):
        is_visited = {}
        for vertex in graph.get_all_vertices():
            is_visited[vertex] = False
        path_priority = [(0, town_idx)]

        while path_priority: # проверка пуст ли, норм?
            min_path = heapq.heappop(path_priority)
            if not is_visited[min_path[1]]:
                is_visited[min_path[1]] = True
                self.__paths[min_path[1]] = min_path[0]
                for edge in graph.get_adj_edges(min_path[1]):
                    if not is_visited[edge['vert_to']]:
                        heapq.heappush(path_priority, (min_path[0] + edge['length'], edge['vert_to']))

    @property
    def paths(self):
        return self.__paths
