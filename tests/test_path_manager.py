import unittest
from source.json_converter import dict_to_graph, read_graph_from_json
from source.game_components.path_manager import PathManager


class TestPathManager(unittest.TestCase):
    def setUp(self):
        self.__small_graph = dict_to_graph(read_graph_from_json('test_graphs/small_graph.json'))
        self.__big_graph = dict_to_graph(read_graph_from_json('test_graphs/big_graph.json'))
        self.__task3_graph = dict_to_graph(read_graph_from_json('test_graphs/task3.json'))

    def test_Dijsktra(self):
        temp_path = PathManager(self.__small_graph, 4)
        self.assertEqual(temp_path.paths, )
        temp_path = PathManager(self.__big_graph, 4)
        self.assertEqual(temp_path.paths, 18)
        temp_path = PathManager(self.__task3_graph, 13)
        self.assertEqual(temp_path.paths, )
