from Graphs.rides_graph import RidesGraph
from Rides.DataAccess.rides_db_context import Session
import networkx as nx
import random
import collections
import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
import numpy as np
import statistics as stats


def calculate_mean_path_length(G):
    print()
    print("Approximated mean shortest path length")
    vertxes = list(G.nodes)
    randA100 = random.choices(vertxes, k=100)
    randB100 = random.choices(vertxes, k=100)
    randA1000 = random.choices(vertxes, k=1000)
    randB1000 = random.choices(vertxes, k=1000)
    randA10000 = random.choices(vertxes, k=10000)
    randB10000 = random.choices(vertxes, k=10000)
    mean100 = 0
    mean1000 = 0
    mean10000 = 0
    for p in range(10000):
        if p < 100:
            mean100 += nx.shortest_path_length(G, randA100[p], randB100[p])
        if p < 1000:
            mean1000 += nx.shortest_path_length(G, randA1000[p], randB1000[p])
        mean10000 += nx.shortest_path_length(G, randA10000[p], randB10000[p])
    mean100 /= 100
    mean1000 /= 1000
    mean10000 /= 10000
    print("Mean path length for 100 random paths:")
    print(mean100)
    print("Mean path length for 1000 random paths:")
    print(mean1000)
    print("Mean path length for 10000 random paths:")
    print(mean10000)


def print_aggregated_degree_distribution(G):
    degree_sequence = sorted(
        [(d, n) for n, d in G.degree()], reverse=True)  # degree sequence
    intervals = [1 ** 1, 5 ** 1, 10 ** 1, 20 ** 1, 40 ** 1, 80 ** 1, 160, 320]
    degree_count = []

    for i in range(len(intervals)):
        min_int = intervals[i - 1] if i > 0 else 0
        max_int = intervals[i]
        degree_count.append(
            sum(map(lambda n: min_int < n[0] < max_int, degree_sequence)))

    print(degree_count)

    # model = LinearRegression()
    # model.fit(np.reshape(intervals, (-1, 1)), degree_count)
    # alpha = model.coef_[0]
    # b = model.intercept_

    # print("alpha: {0}, b: {1}".format(alpha, b))

    fig, ax = plt.subplots()
    ax.plot(intervals, degree_count)
    plt.title("Aggregated degrees")
    plt.ylabel("Count")
    plt.xlabel("Degree")

    ax.set_xticklabels(intervals)
    ax.set_xscale('log')
    ax.set_yscale('log')

    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    plt.axis('off')

    plt.show()

    print()
    # print("10 The most popular nodes are:")
    # current_degree = 1000000
    # i = 0
    # most_popular_nodes = {}
    # while current_degree > 10:
    #     degree = degree_sequence[i][0]
    #     node_id = degree_sequence[i][1]
    #     node = G.nodes(data=True)
    #     if most_popular_nodes[degree] is not None:
    #         most_popular_nodes[degree] = [node]
    #     else:
    #         most_popular_nodes[degree].append(node)
    # print("Player: {0}, tags: {1}".format(degree_sequence[i].User.Id, degree_sequence[i][.Tags))


def print_nodes_degree_distribution(G):
    degree_sequence = sorted([d for n, d in G.degree()],
                             reverse=False)  # degree sequence

    mean = stats.mean(degree_sequence)
    median = stats.median(degree_sequence)
    std_dev = stats.stdev(degree_sequence)

    print()
    print("Degrees mean: {0}".format(mean))
    print("Degrees median: {0}".format(median))
    print("Degrees std deviation: {0}".format(std_dev))
    print("Degrees min: {0}".format(min(degree_sequence)))
    print("Degrees max: {0}".format(max(degree_sequence)))

    degree_count = collections.Counter(degree_sequence)
    deg, cnt = zip(*degree_count.items())

    fig, ax = plt.subplots()
    ax.plot(deg, cnt)

    plt.title("Degrees distribution")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticklabels(deg)
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.show()


def get_average_neighbor_degree(graph):
    return nx.average_neighbor_degree(graph)


def get_nodes_rank(graph):
    poi_nodes = [n
                 for n, d in graph.nodes(data=True) if d['Type'] == 'poi']
    poi_graph = graph.subgraph(poi_nodes)
    ranks = nx.pagerank(poi_graph)
    poi_ranks = list()
    for n, d in poi_graph.nodes(data=True):
        poi_ranks.append((n, ranks[n], d))
    sorted_poi_ranks = sorted(poi_ranks, reverse=True,
                              key=lambda poi_rank: poi_rank[1])

    max_rank = max(poi_ranks, key=lambda poi_rank: poi_rank[1])
    min_rank = min(poi_ranks, key=lambda poi_rank: poi_rank[1])
    step = (max_rank[1] - min_rank[1])/5.0
    return (sorted_poi_ranks, min_rank, max_rank, step)


def get_stats():
    graph = RidesGraph().create_rides_graph(Session())
    print("Is graph bipartite: {0}".format(nx.is_bipartite(graph)))
    # print_aggregated_degree_distribution(graph)
    # print_nodes_degree_distribution(graph)
    # print(get_nodes_rank(graph))
