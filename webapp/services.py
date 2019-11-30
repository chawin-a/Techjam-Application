import operator
import re
from http import HTTPStatus

from flask import Flask, jsonify, request
import math

app = Flask(__name__)

def distance(pos1, pos2):
    return math.sqrt(math.pow(pos1["x"] - pos2["x"], 2) + math.pow(pos1["y"] - pos2["y"], 2))

@app.route("/distance", methods=['POST'])
def calculate_distance():
    body = request.get_json()
    if 'first_pos' not in body or 'second_pos' not in body:
        return '', HTTPStatus.BAD_REQUEST
    pos1 = body['first_pos']
    pos2 = body['second_pos']
    result = distance(pos1, pos2)
    result = f"{result:.3f}"
    return jsonify(distance=result), HTTPStatus.OK


robot_re = re.compile(r"^robot#([1-9][0-9]*)$")

robots = {}

@app.route("/robot/<robot_id>/position", methods=['PUT'])
def update_position(robot_id):
    body = request.get_json()
    if not robot_re.match(robot_id):
        return '', HTTPStatus.BAD_REQUEST

    if robot_id in robots:
        status = HTTPStatus.NO_CONTENT  # 204
    else:
        status = HTTPStatus.CREATED  # 201

    robots[robot_id] = {"position":body['position']}

    return '', HTTPStatus.OK

@app.route("/robot/<robot_id>/position", methods=['GET'])
def get_position(robot_id):
    if not robot_re.match(robot_id):
        return '', HTTPStatus.BAD_REQUEST
    if robot_id not in robots:
        return '', HTTPStatus.NOT_FOUND
    return jsonify(robots[robot_id]), HTTPStatus.OK

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
