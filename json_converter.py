import json
from graph import Graph
from game_components.train import Train


def read_graph_from_json(filename):
    with open(filename) as json_data:
        graph = json.load(json_data)
    return graph


def dict_to_graph(dictionary):
    graph = Graph(idx=dictionary['idx'], name=dictionary['name'])
    for point in dictionary['points']:
        graph.add_vertex(idx=point['idx'], post_idx=point['post_idx'])
    for line in dictionary['lines']:
        graph.add_edge(idx=line['idx'], length=line['length'], vert_from=line['points'][0], vert_to=line['points'][1])
    return graph


def dict_to_trains(dictionary):
    trains = dictionary['trains']
    return [dict_to_train(train) for train in trains]


def dict_to_train(dictionary):
    return Train(idx=dictionary['idx'], speed=dictionary['speed'], line_idx=dictionary['line_idx'],
                 position=dictionary['position'], player_idx=dictionary['player_idx'])
