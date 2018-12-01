import unittest
from source.graph import Graph


class TestGraphMethods(unittest.TestCase):
    def setUp(self):
        self.__graph = Graph(name='test_graph', idx=0)
        self.__graph.add_vertex(1, 1)
        self.__graph.add_vertex(2)
        self.__graph.add_vertex(3)
        self.__graph.add_vertex(4)
        self.__graph.add_edge(1, 0, 1, 2)
        self.__graph.add_edge(2, 0, 1, 3)

        # add this vertices to test edge directions
        self.__graph.add_edge(3, 0, 6, 5)
        self.__graph.add_edge(4, 0, 7, 5)
        self.__graph.add_edge(5, 0, 5, 8)

    def test_getters(self):
        self.assertEqual(self.__graph.name, 'test_graph')
        self.assertEqual(self.__graph.idx, 0)
        self.assertEqual(self.__graph.vert_amnt, 8)

    def test_get_vert(self):
        self.assertEqual(self.__graph.get_all_vertices(), (1, 2, 3, 4, 6, 5, 7, 8))
        self.assertEqual(self.__graph.get_adj_vertices(1), (2, 3))
        self.assertEqual(self.__graph.get_adj_vertices(2), (1,))
        self.assertEqual(self.__graph.get_adj_vertices(4), ())

    def test_get_edge(self):
        self.assertEqual(self.__graph.get_adj_edges(3), [{'edge_idx': 2, 'length': 0, 'vert_to': 1, 'start_vert': 1}])
        self.assertEqual(self.__graph.get_adj_edges(1), [{'edge_idx': 1, 'length': 0, 'vert_to': 2, 'start_vert': 1},
                                                         {'edge_idx': 2, 'length': 0, 'vert_to': 3, 'start_vert': 1}])
        self.assertEqual(self.__graph.get_adj_edges(4), [])

        self.assertEqual(self.__graph.get_edge_by_idx(1), {'length': 0, 'vert_from': 1, 'vert_to': 2})
        self.assertEqual(self.__graph.get_edge_by_idx(2), {'length': 0, 'vert_from': 1, 'vert_to': 3})
        self.assertEqual(self.__graph.get_edge_by_idx(6), None)

        self.assertEqual(self.__graph.get_edge_by_adj_vert(3, 1), {'length': 0, 'edge_idx': 2, 'vert_from': 1, 'vert_to': 3})

    def test_not_add_existing_vert(self):
        self.assertEqual(self.__graph.get_vertex_post_idx(1), 1)
        self.__graph.add_vertex(1, 4)
        self.assertEqual(self.__graph.get_vertex_post_idx(1), 1)

    def test_not_add_existing_edge(self):
        self.assertEqual(self.__graph.get_adj_edges(2), [{'edge_idx': 1, 'length': 0, 'vert_to': 1, 'start_vert': 1}])
        self.__graph.add_edge(3, 0, 1, 2)
        self.assertEqual(self.__graph.get_adj_edges(2), [{'edge_idx': 1, 'length': 0, 'vert_to': 1, 'start_vert': 1}])
        # self.__graph.add_edge(1, 0, 2, 4)
        # self.assertEqual(self.__graph.get_adj_edge(4), [])
        self.__graph.add_edge(5, 0, 4, 4)
        self.assertEqual(self.__graph.get_adj_edges(4), [])

    def test_line_direction(self):
        self.assertEqual(self.__graph.get_edge_by_idx(3), {'length': 0 , 'vert_from': 6, 'vert_to': 5})
        self.assertEqual(self.__graph.get_edge_by_idx(4), {'length': 0, 'vert_from': 7, 'vert_to': 5})
        self.assertEqual(self.__graph.get_edge_by_idx(5), {'length': 0, 'vert_from': 5, 'vert_to': 8})
