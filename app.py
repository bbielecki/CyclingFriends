from flask import Flask
import Users.users_qh as users
import Users.personal_stats_qh as personal_stats
import Rides.rides_qh as rides

app = Flask(__name__)


@app.route('/')
def hello_world():
    # print("users:")
    # print(users.get_users())
    # print("stats:")
    # print(personal_stats.get_stats())
    print(rides.get_rides())
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
