import json
from graph import Graph
from game_components.train import Train
from game_components.game_points import *
from game_components.player import Player
from game_components.lobby import Lobby


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
    return Train(idx=dictionary['idx'], speed=dictionary['speed'], level=dictionary['level'], line_idx=dictionary['line_idx'],
                 position=dictionary['position'], player_idx=dictionary['player_idx'], goods=dictionary['goods'],
                 goods_capacity=dictionary['goods_capacity'], next_level_price=dictionary['next_level_price'])


def dict_to_posts(layer1):
    posts = layer1['posts']
    town = {}
    markets = {}
    storages = {}
    for post in posts:
        if post['type'] == 1:
            town[post['idx']] = dict_to_town(post)
        elif post['type'] == 2:
            markets[post['idx']] = dict_to_market(post)
        elif post['type'] == 3:
            storages[post['idx']] = dict_to_storage(post)
    return town, markets, storages


def dict_to_town(dictionary):
    return Town(idx=dictionary['idx'], point_idx=dictionary['point_idx'], name=dictionary['name'],
                population=dictionary['population'], population_capacity=['population_capacity'],
                armor=dictionary['armor'], armor_capacity=dictionary['armor_capacity'], product=dictionary['product'],
                level=dictionary['level'], next_level_price=dictionary['next_level_price'],
                product_capacity=dictionary['product_capacity'], player_idx=dictionary['player_idx'])


def dict_to_market(dictionary):
    return Market(idx=dictionary['idx'], point_idx=dictionary['point_idx'], name=dictionary['name'],
                  product=dictionary['product'], product_capacity=dictionary['product_capacity'], replenishment=dictionary['replenishment'])


def dict_to_storage(dictionary):
    return Storage(idx=dictionary['idx'], point_idx=dictionary['point_idx'], name=dictionary['name'],
                   replenishment=dictionary['replenishment'], armor=dictionary['armor'], armor_capacity=dictionary['armor_capacity'])


def dict_to_player(dictionary):
    return Player(idx=dictionary['idx'], in_game=dictionary['in_game'],
                  name=dictionary['name'], rating=dictionary['rating'],
                  town=dict_to_town(dictionary['town']))


def dict_to_lobbies(dictionary):
    lobbies = {}
    for game in dictionary['games']:
        lobbies[game['name']] = (dict_to_lobby(game))
    return lobbies


def dict_to_lobby(dictionary):
    return Lobby(name=dictionary['name'], num_players=dictionary['num_players'],
                 num_turns=dictionary['num_turns'], state=dictionary['state'])
