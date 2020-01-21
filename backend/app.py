from flask import Flask, jsonify
from flask_cors import CORS

import Users.users_qh as users
import Users.personal_stats_qh as personal_stats
import Rides.rides_qh as rides
import Graphs.rides_graph as rides_graph
import Rides.pois_qh as pois
import Graphs.rides_graph_stats as stats
import Graphs.rides_users_bipartite_graph_stats as bipartite_users
import Graphs.rides_pois_bipartite_graph_stats as bipartite_pois


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    # pois.add_pois(3928, 10000)
    # stats.get_stats()
    # print(pois.get_pois(10))
    # stats.get_stats()
    # bipartite_users.multiply_graph_nodes()
    bipartite_pois.multiply_graph_nodes()
    return 'Hello World!'


@app.route('/rides', )
def get_rides():
    res = rides.get_rides(500)
    return jsonify(res)


@app.route('/rides/graph')
def get_rides_graph():
    res = rides_graph.get_rides_graph()
    return jsonify(res)


@app.route('/pois', )
def get_pois():
    res = pois.get_pois()
    return jsonify(res)


@app.route('/pois/ranks')
def get_pois_ranks():
    graph = rides_graph.get_users_and_rides_graph()
    res = stats.get_nodes_rank(graph)
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
