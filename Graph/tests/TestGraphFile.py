import unittest
from Graph import Graph


class TestGraphMethods(unittest.TestCase):
    def setUp(self):
        self.__graph = Graph(name='test_graph', idx=0)
        self.__graph.add_vertex(1, 1)
        self.__graph.add_vertex(2)
        self.__graph.add_vertex(3)
        self.__graph.add_vertex(4)
        self.__graph.add_edge(1, 0, 1, 2)
        self.__graph.add_edge(2, 0, 1, 3)

    def test_getters(self):
        self.assertEqual(self.__graph.name, 'test_graph')
        self.assertEqual(self.__graph.idx, 0)
        self.assertEqual(self.__graph.vert_amnt, 4)

    def test_get_vert(self):
        self.assertEqual(self.__graph.get_all_vert(), (1, 2, 3, 4))
        self.assertEqual(self.__graph.get_adj_vert(1), (2, 3))
        self.assertEqual(self.__graph.get_adj_vert(2), (1, ))
        self.assertEqual(self.__graph.get_adj_vert(4), ())

    def test_get_edg(self):
        self.assertEqual(self.__graph.get_adj_edge(3), [{'edge_idx': 2, 'length': 0, 'vert_to': 1}])
        self.assertEqual(self.__graph.get_adj_edge(1), [{'edge_idx': 1, 'length': 0, 'vert_to': 2},
                                                        {'edge_idx': 2, 'length': 0, 'vert_to': 3}])
        self.assertEqual(self.__graph.get_adj_edge(4), [])

    def test_not_add_existing_vert(self):
        self.assertEqual(self.__graph.get_vert_post_idx(1), 1)
        self.__graph.add_vertex(1, 4)
        self.assertEqual(self.__graph.get_vert_post_idx(1), 1)

    def test_not_add_existing_edge(self):
        self.assertEqual(self.__graph.get_adj_edge(2), [{'edge_idx': 1, 'length': 0, 'vert_to': 1}])
        self.__graph.add_edge(3, 0, 1, 2)
        self.assertEqual(self.__graph.get_adj_edge(2), [{'edge_idx': 1, 'length': 0, 'vert_to': 1}])
        # self.__graph.add_edge(1, 0, 2, 4)
        # self.assertEqual(self.__graph.get_adj_edge(4), [])
        self.__graph.add_edge(5, 0, 4, 4)
        self.assertEqual(self.__graph.get_adj_vert(4), [])
