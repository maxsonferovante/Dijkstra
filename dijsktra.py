import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from heapq import heappush
from heapq import heappop


def draw(g, export=False, name='graph'):
    tmp = g.copy()
    for v in tmp.nodes():  # creates an attribute that stores the node number
        tmp.node[v]['label'] = v

    pos = nx.spring_layout(tmp)

    nx.draw(tmp, pos)
    node_labels = nx.get_node_attributes(tmp, 'label')  # gets a list with the labels created
    nx.draw_networkx_labels(tmp, pos, labels=node_labels)  # draw the node number in their respective positions

    if export:
        plt.savefig(name + '.png')
    else:
        plt.show()
    plt.close()


def dijkstra(g, sources):
    tmp = g.copy()
    push = heappush
    pop = heappop
    nodes = tmp.nodes()

    for n in nodes:
        tmp.node[n]['lambda'] = np.Infinity
        tmp.node[n]['pi'] = None

    for _s in sources:
        tmp.node[_s]['lambda'] = 0

    q = []
    s = []

    for n in nodes:
        push(q, (tmp.node[n]['lambda'], n))

    while q:
        u = pop(q)
        u = u[1]
        s.append(u)

        for v in tmp.neighbors(u):
            if v not in s and tmp.node[v]['lambda'] > (tmp.node[u]['lambda'] + g[u][v]['_weight']):
                q.remove((tmp.node[v]['lambda'], v))
                tmp.node[v]['lambda'] = tmp.node[u]['lambda'] + g[u][v]['_weight']
                push(q, (tmp.node[v]['lambda'], v))
                tmp.node[v]['pi'] = u

    h = nx.Graph()
    for u in tmp.nodes():
        h.add_node(u)
        if tmp.node[u]['pi'] is not None:
            h.add_edge(u, tmp.node[u]['pi'])
            h[u][tmp.node[u]['pi']]['_weight'] = tmp[u][tmp.node[u]['pi']]['_weight']
    return h


def read_weighted_adjacency_matrix(path):
    data = np.loadtxt(path)

    rows, cols = np.where(data > 0)

    edges = zip(rows, cols)

    g = nx.Graph(edges)

    for u, v in zip(rows, cols):
        g[u][v]['weight'] = data[u][v]
        g[u][v]['_weight'] = data[u][v]

    return g

arquivo = "adjacentes1.txt"

G = read_weighted_adjacency_matrix(arquivo) ##LEIA A ARQUIVO .TXT 
sources = [] ## escolhe uns vertices ou todos.
tempos = []
for i in range(0,10): 
	begin = timeit.default_timer() ##BAGULHO DO TEMPO
	dijkstra(G, sources)
        end = timeit.default_timer() ##BAGULHO DO TEMPO
        tempos.append((end-begin)/10.0) ## GUARDA O TEMPO DE EXECUÇÃO NA LIST tempos

print(sum(tempos)) ## EXIBE A MEDIA DAS 10 EXECUÇÕES DO ALGORITMO DE PRIM


