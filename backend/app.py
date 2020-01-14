from flask import Flask, jsonify
from flask_cors import CORS

import backend.Users.users_qh as users
import backend.Users.personal_stats_qh as personal_stats
import backend.Rides.rides_qh as rides
import backend.Graphs.rides_graph as rides_graph

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    # print("users:")
    # print(users.get_users())
    # print("stats:")
    # print(personal_stats.get_stats())
    print(rides.get_rides())
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
