from flask import Flask, jsonify
from flask_cors import CORS

import Users.users_qh as users
import Users.personal_stats_qh as personal_stats
import Rides.rides_qh as rides
from osm.get_poi import get_poi
import Graphs.rides_graph as rides_graph

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    # print("users:")
    # print(users.get_users())
    # print("stats:")
    # print(personal_stats.get_stats())
    # print(rides.get_rides())
    print(get_poi(54.349416, 18.648098))
    return 'Hello World!'


@app.route('/rides', )
def get_rides():
    res = rides.get_rides(100)
    return jsonify(res)


@app.route('/rides/graph')
def get_rides_graph():
    res = rides_graph.get_rides_graph()
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
