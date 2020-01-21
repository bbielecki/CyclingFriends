from Graphs.rides_graph import get_users_and_rides_graph
import matplotlib.pyplot as plt
import numpy
import networkx as nx
import statistics as stats
import collections


def multiply_graph_nodes():
    graph = get_users_and_rides_graph()

    users = [(n, d)for n, d in graph.nodes(data=True) if d['Type'] == 'user']
    pois = [(n, d) for n, d in graph.nodes(data=True) if d['Type'] == 'poi']

    print(len(users))
    print(len(pois))

    print()
    print("All users")
    analyze_bipartite_graph(graph, pois, users)

    print()
    print("man vs man")
    analyze_bipartite_graph(graph, pois, users, 1, 1)

    print()
    print("man vs woman")
    analyze_bipartite_graph(graph, pois, users, 1, 2)

    print()
    print("woman vs woman")
    analyze_bipartite_graph(graph, pois, users, 2, 2)

    print()
    print("All users with Garmin")
    analyze_bipartite_graph(graph, pois, users, garmin=True)

    print()
    print("All users without Garmin")
    analyze_bipartite_graph(graph, pois, users, garmin=False)

    print()
    print("man vs woman with Garmin")
    analyze_bipartite_graph(graph, pois, users, 1, 2, garmin=True)

    print()
    print("man vs woman without Garmin")
    analyze_bipartite_graph(graph, pois, users, 1, 2, garmin=False)

    print()
    print("man with garmin vs woman without Garmin")
    analyze_bipartite_graph(graph, pois, users, 1, 2, True, False)

    print()
    print("man without garmin vs woman with Garmin")
    analyze_bipartite_graph(graph, pois, users, 1, 2, False, True)


def analyze_bipartite_graph(graph, pois, users, gender: int = None, gender2: int = None, garmin1: bool = None, garmin2: bool = None):
    graph_matrix = numpy.zeros((len(users), len(pois)))
    print("matrix size: rows {0}, columns {1}".format(len(graph_matrix), len(graph_matrix[0])))

    i = 0
    for u in users:
        j = 0
        for p in pois:
            if graph.has_edge(u[0], p[0]) or graph.has_edge(p[0], u[0]):
                graph_matrix[i][j] += 1
            j += 1
        i += 1

    transposed = numpy.transpose(graph_matrix)
    bipartite = numpy.matmul(graph_matrix, transposed)
    for i in range(bipartite.shape[0]):
        bipartite[i][i] = 0

    numpy.savetxt('users_correlation.txt', bipartite, fmt='%s')
    c_users = find_connected_users(bipartite, users, gender, gender2, garmin1, garmin2)
    max_connected = bipartite.max()

    connected_users_graph(c_users)

    print("Max connected: {0}".format(max_connected))
    print_connected_users_distribution(c_users, max_connected, gender, gender2, garmin1, garmin2)


def find_connected_users(bipartite, users, gender: int = None, gender2: int = None, garmin1: bool = None, garmin2: bool = None):
    connected_users = []

    for i in range(bipartite.shape[0]):
        j = i
        while j < bipartite.shape[1]:
            if bipartite[i][j] > 1:
                if gender is not None and gender2 is not None and \
                        ((users[i][1]["UserGender"] == gender and users[i][1]["UserHasGarmin"] == garmin1 and
                          users[j][1]["UserGender"] == gender2 and users[j][1]["UserHasGarmin"] == garmin1) or
                         (users[j][1]["UserGender"] == gender and users[j][1]["UserHasGarmin"] == garmin1 and
                          users[i][1]["UserGender"] == gender2 and users[i][1]["UserHasGarmin"] == garmin1)):
                    # if garmin1 is not None and \
                    #         (users[i][1]["UserHasGarmin"] == garmin1 and users[j][1]["UserHasGarmin"] == garmin2):
                    connected_users.append((users[i], users[j], bipartite[i][j]))
                    if garmin1 is None:
                        connected_users.append((users[i], users[j], bipartite[i][j]))

                if gender is None and gender2 is None:
                    if garmin1 is not None and \
                            (users[i][1]["UserHasGarmin"] == garmin1 and users[j][1]["UserHasGarmin"] == garmin1):
                        connected_users.append((users[i], users[j], bipartite[i][j]))
                    if garmin1 is None:
                        connected_users.append((users[i], users[j], bipartite[i][j]))
            j += 1

    return connected_users


def find_connected_pois(bipartite, users, gender: int = None, gender2: int = None, garmin: bool = None):
    connected_pois = []

    for i in range(bipartite.shape[1]):
        j = i
        while j < bipartite.shape[0]:
            if bipartite[j][i] > 1:
                if gender is not None and gender2 is not None and \
                        ((users[i][1]["UserGender"] == gender and users[j][1]["UserGender"] == gender2) or
                         (users[j][1]["UserGender"] == gender and users[i][1]["UserGender"] == gender2)):
                    if garmin is not None and \
                            (users[i][1]["UserHasGarmin"] == garmin and users[j][1]["UserHasGarmin"] == garmin):
                        connected_pois.append(
                            (users[i], users[j], bipartite[i][j]))
                    if garmin is None:
                        connected_pois.append(
                            (users[i], users[j], bipartite[i][j]))

                if gender is None and gender2 is None:
                    if garmin is not None and \
                            (users[i][1]["UserHasGarmin"] == garmin and users[j][1]["UserHasGarmin"] == garmin):
                        connected_pois.append(
                            (users[i], users[j], bipartite[i][j]))
                    if garmin is None:
                        connected_pois.append(
                            (users[i], users[j], bipartite[i][j]))
            j += 1

    return connected_pois


def print_connected_users_distribution(connected_users, max_connected,  gender: int = None, gender2: int = None, garmin1: bool = None, garmin2: bool = None):
    connections = []

    for i in range(1, int(max_connected)):
        l = len([(a, b, c) for a, b, c in connected_users if c > i])
        connections.append(l)
        print("number connected users more than {0} times: {1}".format(i, l))

    fig, ax = plt.subplots()
    ax.plot(range(1, int(max_connected)), connections)
    plt.title("Users meeting frequency {0} {1} {2} {3}".format(gender, gender2, garmin1, garmin2))
    plt.ylabel("Pairs count")
    plt.xlabel("Number of meetings")

    ax.set_yscale('log')

    plt.show()


def connected_users_graph(connected_users):
    g = nx.Graph()

    for u in connected_users:
        if not g.has_edge(u[0][0], u[1][0]) or not g.has_edge(u[1][0], u[0][0]):
            g.add_edge(u[0][0], u[1][0])
            # g.add_edge(u[1][0], u[0][0])

    options = {
        'node_color': 'black',
        'node_size': 1,
        'line_color': 'grey',
        'linewidths': 0,
        'width': 0.1,
    }
    nx.draw_circular(g, **options)
    print_aggregated_degree_distribution(g)
    print_nodes_degree_distribution(g)


def print_aggregated_degree_distribution(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    intervals = [10 ** 1, 10 ** 1.25, 10 ** 1.5, 10 ** 1.75, 10 ** 2, 10 ** 2.25, 10 ** 2.5, 10 ** 2.75, 10 ** 3, 10 ** 3.25, 10 ** 3.5, 10 ** 3.75, 10 ** 4, 10 ** 4.25, 10 ** 4.5, 10 ** 5]
    degree_count = []

    for i in range(len(intervals)):
        min_int = intervals[i - 1] if i > 0 else 0
        max_int = intervals[i]
        degree_count.append(len([x for x in degree_sequence if min_int < x < max_int]))

    print(degree_count)

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


def print_nodes_degree_distribution(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=False)  # degree sequence

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