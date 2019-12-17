from flask import Flask
import Users.users_qh as users

app = Flask(__name__)


@app.route('/')
def hello_world():
    print(users.result)
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
