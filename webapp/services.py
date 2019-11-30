import operator
import re
from http import HTTPStatus

from flask import Flask, jsonify, request
import math

robot_re = re.compile(r"^robot#([1-9][0-9]*)$")
robots = {}

app = Flask(__name__)
def distance(pos1, pos2, metric="euclidean"):
    try:
        print(pos1)
        print(pos2)
        if metric == "manhattan":
            p = 1
        elif metric == "euclidean":
            p = 2
        else:
            raise Exception("Error")
        return math.pow(math.pow(pos1["x"] - pos2["x"], p) + math.pow(pos1["y"] - pos2["y"], p),(1/p))
    except:
        raise Exception("Error")

def _get_position(obj):
    if 'x' in obj and 'y' in obj:
        return obj
    elif isinstance(obj, str):
        if robot_re.match(obj):
            _id = int(obj.split('#')[1])
            if _id in robots:
                return robots[_id]
            else:
                raise Exception("Error")
        else:
            raise Exception("Error")
    else:
        raise Exception("Error")


@app.route("/distance", methods=['POST'])
def calculate_distance():
    body = request.get_json()
    met = "euclidean"
    if 'first_pos' not in body or 'second_pos' not in body:
        return '', HTTPStatus.BAD_REQUEST
    if 'metric' in body:
        met = body['metric']
    try:
        pos1 = _get_position(body['first_pos'])
        pos2 = _get_position(body['second_pos'])
    except:
        return '', HTTPStatus.BAD_REQUEST

    try:
        result = distance(pos1, pos2, met)
    except:
        return '', HTTPStatus.FAILED_DEPENDENCY
    result = f"{result:.3f}"
    return jsonify(distance=result), HTTPStatus.OK

@app.route("/robot/<robot_id>/position", methods=['PUT'])
def update_position(robot_id):
    body = request.get_json()
    try:
        _id = int(robot_id)
    except:
        return '', HTTPStatus.BAD_REQUEST

    if _id < 1 or _id > 999999:
        return '', HTTPStatus.BAD_REQUEST

    # if _id in robots:
    #     status = HTTPStatus.NO_CONTENT  # 204
    # else:
    #     status = HTTPStatus.CREATED  # 201

    robots[_id] = body['position']

    return '', HTTPStatus.NO_CONTENT

@app.route("/robot/<robot_id>/position", methods=['GET'])
def get_position(robot_id):
    
    try:
        _id = int(robot_id)
    except:
        return '', HTTPStatus.BAD_REQUEST
    
    if _id < 1 or _id > 999999:
        return '', HTTPStatus.BAD_REQUEST

    if _id not in robots:
        return '', HTTPStatus.NOT_FOUND

    return jsonify(position=robots[_id]), HTTPStatus.OK


@app.route("/nearest", methods=['POST'])
def get_nearest():
    body = request.get_json()

    if "ref_position" not in body:
        return '', HTTPStatus.BAD_REQUEST
    ref = body["ref_position"]
    print(ref)
    try:
        result = []
        dis = 999999999999
        print("esfjlsdf")
        print(robots)
        for robot, position in robots.items():
            print(robot)
            print(position)
            d = distance(position, ref)
            if dis > d + 1e-9:
                dis = d
                result = []
            if d >= dis - 1e-9 and d <= dis + 1e-9:
                result.append(robot)
    except:
        return '', HTTPStatus.BAD_REQUEST

    return jsonify(robot_ids=result), HTTPStatus.OK



# @app.route("/robot/<robot_id>/position", methods='PUT')
# def update_position(robot_id):
#     if not robot_re.match(robot_id):
#         return '', HTTPStatus.BAD_REQUEST
#     body = request.get_json()
#     return '', HTTPStatus.OK

# variable_re = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
# func_map = {
#     '+': operator.add,
#     '-': operator.sub,
#     '*': operator.mul,
#     '/': operator.truediv,
# }

# variables = {}


# @app.route("/calc", methods=['POST'])
# def calculate_expression():
#     body = request.get_json()
#     left, op, right = body['expression'].split()

#     left = _get_value(left)
#     right = _get_value(right)

#     result = func_map[op](left, right)
#     result = f"{result:.2f}"
#     return jsonify(result=result), HTTPStatus.OK


# def _get_value(token):
#     if variable_re.fullmatch(token):
#         value = variables[token]
#     else:
#         value = token
#     return float(value)


# @app.route("/variable/<name>", methods=['PUT'])
# def put_variable(name):
#     body = request.get_json()
#     if name in variables:
#         status = HTTPStatus.NO_CONTENT  # 204
#     else:
#         status = HTTPStatus.CREATED  # 201
#     variables[name] = body['value']
#     return '', status


# @app.route("/variable/<name>", methods=['GET'])
# def get_variable(name):
#     if name not in variables:
#         return '', HTTPStatus.NOT_FOUND
#     value = variables[name]
#     value = f"{float(value):.2f}"
#     return jsonify(value=value), HTTPStatus.OK
