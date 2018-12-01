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

    def dijkstra(self, graph, town_idx):
        is_visited = {}
        for vertex in graph.get_all_vertices():
            is_visited[vertex] = False
        path_priority = [(0, town_idx)]

        while path_priority: # проверка пуст ли, норм?
            min = heapq.heappop(path_priority)
            if not is_visited[min[1]]:
                is_visited[min[1]] = True
                self.__paths[min[1]] = min[0]
                for vertex in graph.get_adj_vertices(min[1]):
                    if not is_visited[vertex]:
                        heapq.heappush(path_priority, (min[0] + 1, vertex))
