import json
from source.graph import Graph
from source.game_components.train import Train
from source.game_components.game_points import *


def read_graph_from_json(filename):
    with open(filename) as json_data:
        graph = json.load(json_data)
    return graph

  
def dict_to_graph(layer0):
    graph = Graph(idx=layer0['idx'], name=layer0['name'])
    for point in layer0['points']:
        graph.add_vertex(idx=point['idx'], post_idx=point['post_idx'])
    for line in layer0['lines']:
        graph.add_edge(idx=line['idx'], length=line['length'], vert_from=line['points'][0], vert_to=line['points'][1])
    return graph


def dict_to_trains(layer1):
    trains = {}
    for train in layer1['trains']:
        trains[train['idx']] = dict_to_train(train)
    return trains


def dict_to_train(dictionary):
    return Train(idx=dictionary['idx'], speed=dictionary['speed'], line_idx=dictionary['line_idx'],
                 position=dictionary['position'], player_idx=dictionary['player_idx'], goods=dictionary['goods'],
                 goods_capacity=dictionary['goods_capacity'])


def dict_to_posts(layer1):
    posts = layer1['posts']
    result = {}
    for post in posts:
        if post['type'] == 1:
            result[post['idx']] = dict_to_town(post)
        elif post['type'] == 2:
            result[post['idx']] = dict_to_market(post)
        elif post['type'] == 3:
            result[post['idx']] = dict_to_storage(post)
    return result


def dict_to_town(dictionary):
    return Town(idx=dictionary['idx'], point_idx=dictionary['point_idx'], name=dictionary['name'], population=dictionary['population'], population_capacity=['population_capacity'],
                armor=dictionary['armor'], armor_capacity=dictionary['armor_capacity'], product=dictionary['product'],
                product_capacity=dictionary['product_capacity'])


def dict_to_market(dictionary):
    return Market(idx=dictionary['idx'], point_idx=dictionary['point_idx'], name=dictionary['name'],
                  product=dictionary['product'], product_capacity=dictionary['product_capacity'], replenishment=dictionary['replenishment'])


def dict_to_storage(dictionary):
    return Storage(idx=dictionary['idx'], point_idx=dictionary['point_idx'], name=dictionary['name'],
                   replenishment=dictionary['replenishment'], armor=dictionary['armor'], armor_capacity=dictionary['armor_capacity'])
