from werkzeug import Response
from funcationalities.problemLinks import problems
from flask import Flask, jsonify, request
import time
import os

app = Flask(__name__)

DATABSE_PATH = os.path.join(os.path.dirname(
    __file__), "funcationalities", "database")


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/getProblemLinks')
def callProblems():
    start = time.time()
    userlist = request.args.get('userlist').split(',')
    userlist = list(map(lambda x: x.lower(), userlist))
    low = int(request.args.get('low'))
    high = int(request.args.get('high'))
    need = int(request.args.get('need'))
    # refresh argument input lena hai
    obj = problems(False)
    temp = obj.getProblemLinks(low, high, userlist, need)
    print(f"{time.time() - start} s for request")
    return jsonify(temp)


@app.route("/files")
def getFiles():
    itemsList = os.listdir(DATABSE_PATH)
    return jsonify(itemsList)


@app.route("/test")
def test():
    res = ""
    for k, v in request.args.items():
        res += f"{k} : {v}\n"
    return Response(res)


if __name__ == '__main__':
    app.run(debug=True)
