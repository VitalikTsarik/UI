import unittest
from source.json_converter import dict_to_graph, read_graph_from_json
from source.game_components.path_manager import PathManager


class TestPathManager(unittest.TestCase):
    def setUp(self):
        self.__small_graph = dict_to_graph(read_graph_from_json('../test_graphs/small_graph.json'))
        self.__big_graph = dict_to_graph(read_graph_from_json('../test_graphs/my_graph.json'))
        self.__task3_graph = dict_to_graph(read_graph_from_json('../test_graphs/task3.json'))

    def test_Dijsktra(self):
        self.assertEqual(PathManager().min_paths_from_town(self.__small_graph, 4), ({4: 0, 3: 1, 10: 1, 9: 2, 11: 2, 5: 3, 8: 4, 2: 3, 12: 5, 7: 5, 1: 5, 6: 4},
                                                                                    {4: -1, 3: 4, 10: 4, 9: 3, 11: 10, 5: 4, 8: 2, 2: 3, 12: 11, 7: 8, 1: 2, 6: 5}))

        self.assertEqual(PathManager().min_paths_from_town(self.__big_graph, 2), ({2: 0, 9: 1, 3: 1, 7: 1, 4: 2, 5: 3, 6: 3},
                                                                                  {2: -1, 9: 2, 3: 2, 7: 2, 4: 3, 5: 3, 6: 7}))

        self.assertEqual(PathManager().min_paths_from_town(self.__task3_graph, 13), ({13: 0, 19: 1, 14: 2, 20: 2, 24: 2, 18: 3, 15: 4, 21: 4, 17: 4, 16: 5, 23: 5, 22: 6},
                                                                                     {13: -1, 19: 13, 14: 13, 20: 19, 24: 19, 18: 13, 15: 14, 21: 20, 17: 18, 16: 15, 23: 17, 22: 16}))
