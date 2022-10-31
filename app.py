from werkzeug import Response
from funcationalities.problemLinks import problems
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/getProblemLinks')
def callProblems():
    
    userlist = request.args.get('userlist').split(',')
    low = int(request.args.get('low'))
    high = int(request.args.get('high'))
    need = int(request.args.get('need'))
    obj = problems()
    return jsonify(obj.getProblemLinks(low, high, userlist, need))


@app.route("/test")
def test():
    res = ""
    for k,v in request.args.items() :
        res+=f"{k} : {v}\n"
    return Response(res)


if __name__ == '__main__':
    app.run(debug=True)
