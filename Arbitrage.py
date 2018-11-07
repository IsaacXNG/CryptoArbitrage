import requests

transaction_fee = 0.005
major_currencies = ["DOGE"]
ignore_currencies = []

try:
    markets = requests.get("https://www.cryptopia.co.nz/api/GetMarkets").json()
    if not markets["Success"]:
        exit()
except:
    exit()


class graph:
    """
    Directed Cyclical Digraph
    """
    def __init__(self):
        self.currencies = {} #dictionary that maps currency name to currency objects

        for i in markets['Data']:
            if i["Volume"] > 0:
                coin1, coin2 = i["Label"].split("/")
                if coin1 in ignore_currencies or coin2 in ignore_currencies:
                    continue
                if coin1 not in self.currencies.keys():
                    self.currencies[coin1] = node(coin1)
                if coin2 not in self.currencies.keys():
                    self.currencies[coin2] = node(coin2)

                self.currencies[coin1].addChildren(self.currencies[coin2], i["BidPrice"])
                self.currencies[coin2].addChildren(self.currencies[coin1], 1/i["AskPrice"])

    def __repr__(self):
        return str(self.currencies)

class node:
    def __init__(self, name):
        self.name = name
        self.children = {} #dictionary that maps transactions to their price (e.g, if 1 unit of X gives 10 units of Y then we have {Y:10})

    def __repr__(self):
        return self.name

    def addChildren(self, newNode, conversion_rate):
        self.children[newNode] = conversion_rate

    def printChildren(self):
        print(str(self.children))

accumulator = {}

def find_good_cycles(graph):
    for currency in major_currencies:
        dfs([graph.currencies[currency]], 1, max_depth = 4)

def dfs(visited, conversion_product, max_depth):
    if(max_depth <= 0):
        return
    for nextNode, conversion_rate in visited[-1].children.items():
        p = (1 - transaction_fee)*conversion_rate*conversion_product

        if nextNode in visited:
            if len(visited) > 3 and visited[0] == nextNode and p > 1:
                accumulator[tuple(visited + [nextNode])] = p
        else:
            newVisited = list(visited)
            newVisited.append(nextNode)
            dfs(newVisited, p, max_depth - 1)

g = graph()
find_good_cycles(g)

sorted_list = sorted(accumulator.items(), key=lambda kv: kv[1], reverse=True)
for item in sorted_list:
    print(item)





