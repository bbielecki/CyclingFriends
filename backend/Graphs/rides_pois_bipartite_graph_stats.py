from Graphs.rides_graph import get_users_and_rides_graph
import matplotlib.pyplot as plt
import numpy


def multiply_graph_nodes():
    graph = get_users_and_rides_graph()

    users = [(n, d)for n, d in graph.nodes(data=True) if d['Type'] == 'user']
    pois = [(n, d) for n, d in graph.nodes(data=True) if d['Type'] == 'poi']

    print(len(users))
    print(len(pois))

    print()
    print("All user")
    analyze_bipartite_graph(graph, pois, users)

    print()
    print("man")
    analyze_bipartite_graph(graph, pois, users, 1)

    print()
    print("woman")
    analyze_bipartite_graph(graph, pois, users, 2)

    print()
    print("All users with Garmin")
    analyze_bipartite_graph(graph, pois, users, garmin=True)

    print()
    print("All users without Garmin")
    analyze_bipartite_graph(graph, pois, users, garmin=False)

    print()
    print("40 <= weight < 60")
    analyze_bipartite_graph(graph, pois, users, weight=(50, 70))

    print()
    print("60 <= weight < 80")
    analyze_bipartite_graph(graph, pois, users, weight=(60, 80))

    print()
    print("80 <= weight < 100")
    analyze_bipartite_graph(graph, pois, users, weight=(80, 100))


def analyze_bipartite_graph(graph, pois, users, gender: int = None, weight: (int, int) = None, garmin: bool = None):
    graph_matrix = numpy.zeros((len(pois), len(users)))
    print("matrix size: rows {0}, columns {1}".format(
        len(graph_matrix), len(graph_matrix[0])))

    i = 0
    for p in pois:
        j = 0
        for u in users:
            if graph.has_edge(u[0], p[0]) or graph.has_edge(p[0], u[0]):
                if garmin is not None and gender is not None:
                    if u[1]['UserHasGarmin'] == garmin and u[1]['UserGender'] == gender:
                        if weight is None:
                            graph_matrix[i][j] += 1
                        else:
                            user_weight = u[1]['UserWeight']
                            if user_weight >= weight[0] and user_weight <= weight[1]:
                                graph_matrix[i][j] += 1
                if garmin is None and gender is None:
                    if weight is None:
                        graph_matrix[i][j] += 1
                    else:
                        user_weight = u[1]['UserWeight']
                        if user_weight >= weight[0] and user_weight <= weight[1]:
                            graph_matrix[i][j] += 1
                if garmin is None and gender is not None:
                    if u[1]['UserGender'] == gender:
                        if weight is None:
                            graph_matrix[i][j] += 1
                        else:
                            user_weight = u[1]['UserWeight']
                            if user_weight >= weight[0] and user_weight <= weight[1]:
                                graph_matrix[i][j] += 1
                if garmin is not None and gender is None:
                    if u[1]['UserHasGarmin'] == garmin:
                        if weight is None:
                            graph_matrix[i][j] += 1
                        else:
                            user_weight = u[1]['UserWeight']
                            if user_weight >= weight[0] and user_weight <= weight[1]:
                                graph_matrix[i][j] += 1

            j += 1
        i += 1

    transposed = numpy.transpose(graph_matrix)
    bipartite = numpy.matmul(graph_matrix, transposed)
    for i in range(bipartite.shape[0]):
        bipartite[i][i] = 0

    numpy.savetxt('pois_correlation.txt', bipartite, fmt='%s')
    c_pois = find_connected_pois(bipartite, pois)
    max_connected = bipartite.max()

    print("Max connected: {0}".format(max_connected))
    print_connected_pois_distribution(
        c_pois, max_connected, gender, weight, garmin)


def find_connected_pois(bipartite, pois):
    connected_pois = []

    for i in range(bipartite.shape[0]):
        j = i
        while j < bipartite.shape[1]:
            if bipartite[i][j] > 1:
                connected_pois.append((pois[i], pois[j], bipartite[i][j]))
            j += 1

    return connected_pois


def print_connected_pois_distribution(connected_pois, max_connected,  gender: int = None, weight: (int, int) = None, garmin: bool = None):
    connections = []

    for i in range(1, int(max_connected)):
        l = len([(a, b, c) for a, b, c in connected_pois if c > i])
        connections.append(l)
        print(
            "Number of pois with users more than {0} times: {1}".format(i, l))

    fig, ax = plt.subplots()
    ax.plot(range(1, int(max_connected)), connections)
    plt.title("Pois users {0} {1} {2}".format(
        gender, weight, garmin))
    plt.ylabel("Users count")
    plt.xlabel("Number of pois")

    ax.set_yscale('log')

    plt.show()
