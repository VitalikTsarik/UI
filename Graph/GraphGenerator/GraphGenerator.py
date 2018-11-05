import json
from random import randint

idx = '5'
name = 'map05'
lines_idx_range = 150
lines_length_range = 50
min_num_of_lines = 10
points_idx_range = 100
points_post_idx_range = 100
min_num_of_points = 10

graph = {'idx': idx, 'name': name, 'points': [], 'lines': []}

poinst_num = randint(min_num_of_points, points_idx_range)
idxs = set()
for i in range(0, poinst_num):
    idxs.add(randint(0, lines_idx_range))

poinst_num = len(idxs)

for i in range(0, poinst_num):
    graph['points'].append({
        'idx': idxs.pop(),
        'post_idx': randint(0, points_post_idx_range)
    })

for i in range(0, randint(min_num_of_lines, lines_idx_range)):
    p1 = randint(0, poinst_num - 1)
    p2 = randint(0, poinst_num - 1)
    while p1 == p2:
        p2 = randint(0, poinst_num - 1)
    graph['lines'].append({
        'idx': randint(0, lines_idx_range),
        'length': randint(1, lines_length_range),
        'points': [graph['points'][p1]['idx'], graph['points'][p2]['idx']]
                           })

with open('{}.json'.format(name), 'w') as outfile:
    json.dump(graph, outfile)
