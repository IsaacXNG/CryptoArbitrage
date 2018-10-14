import requests
import numpy as np
import pandas as pd

import os
import json

n_tuples = 25

if os.path.isfile("markets.json"):
    with open('markets.json') as input:
        markets = json.load(input)
else:
    markets = requests.get("https://www.cryptopia.co.nz/api/GetMarkets").json()
    with open('markets.json', 'w') as output:
        json.dump(markets, output)

key_table = {}
adjacency_matrix = None

for i in markets['Data']:
    if i["Volume"] > 0:
        x,y = i["Label"].split("/")
        if x not in key_table.keys():
            key_table[x] = len(key_table)
        if y not in key_table.keys():
            key_table[y] = len(key_table)

adjacency_matrix = np.zeros((len(key_table),len(key_table)), dtype=float)

for i in markets['Data']:
    if i["Volume"] > 0:
        x,y = i["Label"].split("/")
        adjacency_matrix[key_table[x]][key_table[y]] = i["BidPrice"]
        adjacency_matrix[key_table[y]][key_table[x]] = 1/i["AskPrice"]

adjacency_matrix = np.array(adjacency_matrix)
adjacency_matrix = adjacency_matrix[:n_tuples ,:n_tuples ]

keys = []
for item in key_table.keys():
    keys.append(item)

#Save adjacency matrix to CSV
csv = pd.DataFrame(adjacency_matrix)
csv.columns = keys[:n_tuples]
csv.index = keys[:n_tuples ]
csv.to_csv("view.csv")

sample_matrix = np.array([[1, 0.741, 0.657, 1.061, 1.005],
                        [1.349, 1, 0.888, 1.433, 1.366],
                        [1.521, 1.126, 1, 1.614, 1.538],
                        [0.942, 0.698, 0.619, 1, 0.953],
                         [0.995, 0.732, 0.650, 1.049, 1]])

cycle_accumulator = []

def find_good_cycles(graph):
    original = graph.copy()
    for i in np.arange(graph.shape[0]):
        for j in np.arange(graph.shape[0]):
            graph[i][j] = np.log(graph[i][j] + 0.0000000000001)

    dfs(original, graph, 0, [])

#Depth first search to find cycles where the sum of the logs are greater than zero, getting a net positive yield
def dfs(original, graph, current_v, visited):
    if current_v in visited:
        if len(visited) <= 3:
            return
        tally = [current_v]
        iter = visited.pop()
        while iter != current_v:
            tally.append(iter)
            iter = visited.pop()
        tally.append(iter)
        tally.reverse()
        sum = 0
        for i in np.arange(len(tally)-1):
            value = original[tally[i]][tally[i+1]]
            if value == 0:
                return
            else:
                sum += graph[tally[i]][tally[i+1]]

        if sum > 0 and len(tally) > 3:
            cycle_accumulator.append((tally, sum))
    else:
        visited.append(current_v)
        for i in np.arange(graph.shape[0]):
            if original[current_v][i] != 0 and current_v != i:
                dfs(original, graph, i, list(visited))

find_good_cycles(adjacency_matrix)

reverse_key_table = {}
i = 0
for key in key_table.keys():
    reverse_key_table[i] = key
    i += 1

for element in cycle_accumulator:
    gain_score = element[1]
    cycle_path = element[0]

    real_names = ""
    for i in cycle_path:
        real_names = real_names + " -> " + (reverse_key_table[i])
    print(cycle_path, real_names, " log-gain-score:", gain_score)





