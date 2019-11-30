import operator
import re
from http import HTTPStatus
import os

from flask import Flask, jsonify, request
import math

robot_re = re.compile(r"^robot#([1-9][0-9]*)$")
robots = {}

app = Flask(__name__)
def distance(pos1, pos2, metric="euclidean"):
    try:
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
    k = 1
    if "k" in body:
        try:
            k = int(body["k"])
        except:
            return '', HTTPStatus.BAD_REQUEST
    ref = body["ref_position"]

    try:
        result = []
        dis = 999999999999
        d = [ (distance(position, ref), robot) for robot, position in robots.items()]
        d.sort()
        result = [i[1] for i in d[:k]]
            # d = distance(position, ref)
            # if dis > d:
            #     dis = d
            #     result = [robot]
    except:
        return '', HTTPStatus.BAD_REQUEST

    return jsonify(robot_ids=result), HTTPStatus.OK

@app.route("/closestpair", methods=['GET'])
def closest_pair():
    n = len(robots) 
    if len(robots) < 2:
        return '', HTTPStatus.FAILED_DEPENDENCY
    f = open('webapp/in', "w")
    f.write(str(n)+'\n')
    for robot, position in robots.items():
        f.write(str(position["x"]) + " " + str(position["y"])+"\n")
    f.close()
    output = float(os.popen('webapp/closestpair < webapp/in').read())
    return jsonify(distance=f"{output:.3f}"), HTTPStatus.OK  
