# todo: проверять тип того, что передаём в методы
class Graph(object):
    def __init__(self, name, idx):
        self.__graph = {}
        self.__name = name
        self.__idx = idx

    @property
    def name(self):
        return self.__name

    @property
    def idx(self):
        return self.__idx

    @property
    def vert_amnt(self):
        return len(self.__graph)

    # warning попытка добавить existing вершину
    def add_vertex(self, idx, post_idx=None):
        if idx not in self.__graph.keys():
            self.__graph[idx] = {
                'post_idx': post_idx,
                'adj_edge': []
            }

    # warning попытка добавить existing edge
    def add_edge(self, idx, length, vert_from, vert_to):
        if vert_from == vert_to:
            return
        if vert_from in self.__graph.keys():
            for vertex in self.__graph[vert_from]['adj_edge']:
                if vertex['vert_to'] == vert_to:
                    return
        else:
            self.add_vertex(vert_from)

        self.__graph[vert_from]['adj_edge'].append(
            {
                'edge_idx': idx,
                'length': length,
                'vert_to': vert_to,
                'start_vert': vert_from
            }
        )

        if vert_to not in self.__graph.keys():
            self.add_vertex(vert_to)
        self.__graph[vert_to]['adj_edge'].append(
            {
                'edge_idx': idx,
                'length': length,
                'vert_to': vert_from,
                'start_vert': vert_from
            }
        )

    def get_all_vertices(self):
        return tuple(self.__graph.keys())

    def get_adj_edges(self, idx):
        return self.__graph[idx]['adj_edge']

    def get_adj_vertices(self, idx):
        return tuple([edge['vert_to'] for edge in self.__graph[idx]['adj_edge']])

    def get_vertex_post_idx(self, idx):
        return self.__graph[idx]['post_idx']

    def get_edge_by_idx(self, idx):
        for vert in self.__graph.keys():
            for edge in self.__graph[vert]['adj_edge']:
                if edge['edge_idx'] == idx:
                    return {'length': edge['length'],
                            'vert_from': edge['start_vert'],
                            'vert_to': edge['vert_to'] if edge['start_vert'] != edge['vert_to'] else vert}

    def get_edge_by_adj_vert(self, vert1, vert2):
        for edge in self.__graph[vert1]['adj_edge']:
            if edge['vert_to'] == vert2:
                return {'length': edge['length'],
                        'edge_idx': edge['edge_idx'],
                        'vert_from': edge['start_vert'],
                        'vert_to': vert1 if edge['start_vert'] != vert1 else vert2}
