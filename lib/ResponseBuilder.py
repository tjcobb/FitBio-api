from flask import jsonify, make_response


def success(body):
    return build_response(200, body)


def failure(body):
    return build_response(500, body)


def build_response(status_code, body):
    resp = make_response(jsonify(body), status_code)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = True
    return resp
