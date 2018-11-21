import json
from source.graph import Graph


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
