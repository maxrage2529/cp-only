from werkzeug import Response
from funcationalities.problemLinks import problems
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/<int:n>')
def callProblems(n):
    userlist = ["maxrage", "Dev_Manus",
                "Dipankar_Kumar_Singh", "akashsingh_10"]

    low = 1400
    high = 1600
    need = 1
    obj = problems()
    return jsonify(obj.getProblemLinks(low, high, userlist, need))


@app.route("/test")
def test():
    print(request.args.get("username", None))
    return Response("Test")


if __name__ == '__main__':
    app.run(debug=True)
