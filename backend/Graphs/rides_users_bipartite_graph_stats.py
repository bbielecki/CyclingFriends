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


def analyze_bipartite_graph(graph, pois, users, gender: int = None, gender2: int = None, garmin: bool = None):
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
    c_users = find_connected_users(bipartite, users, gender, gender2, garmin)
    max_connected = bipartite.max()

    print("Max connected: {0}".format(max_connected))
    print_connected_users_distribution(c_users, max_connected)


def find_connected_users(bipartite, users, gender: int = None, gender2: int = None, garmin: bool = None):
    connected_users = []

    for i in range(bipartite.shape[0]):
        j = i
        while j < bipartite.shape[1]:
            if bipartite[i][j] > 1:
                if gender is not None and gender2 is not None and \
                        ((users[i][1]["UserGender"] == gender and users[j][1]["UserGender"] == gender2) or
                         (users[j][1]["UserGender"] == gender and users[i][1]["UserGender"] == gender2)):
                    if garmin is not None and \
                            (users[i][1]["UserHasGarmin"] == garmin and users[j][1]["UserHasGarmin"] == garmin):
                        connected_users.append((users[i], users[j], bipartite[i][j]))
                    if garmin is None:
                        connected_users.append((users[i], users[j], bipartite[i][j]))

                if gender is None and gender2 is None:
                    if garmin is not None and \
                            (users[i][1]["UserHasGarmin"] == garmin and users[j][1]["UserHasGarmin"] == garmin):
                        connected_users.append((users[i], users[j], bipartite[i][j]))
                    if garmin is None:
                        connected_users.append((users[i], users[j], bipartite[i][j]))
            j += 1

    return connected_users


def print_connected_users_distribution(connected_users, max_connected,  gender: int = None, gender2: int = None, garmin: bool = None):
    connections = []

    for i in range(1, int(max_connected)):
        l = len([(a, b, c) for a, b, c in connected_users if c > i])
        connections.append(l)
        print("number connected users more than {0} times: {1}".format(i, l))

    fig, ax = plt.subplots()
    ax.plot(range(1, int(max_connected)), connections)
    plt.title("Users meeting frequency {0} {1} {2}".format(gender, gender2, garmin))
    plt.ylabel("Pairs count")
    plt.xlabel("Number of meetings")

    ax.set_yscale('log')

    plt.show()


