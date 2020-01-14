from flask import Flask, jsonify
from flask_cors import CORS

# import Users.users_qh as users
# import Users.personal_stats_qh as personal_stats
# import Rides.rides_qh as rides
# import Graphs.rides_graph as rides_graph

import Rides.pois_qh as pois

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    pois.add_pois()
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
