import datetime
import json
from cerberus import Validator
from flask import request, Response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from mongoengine import DoesNotExist

from src import app
from src.models.User import User


def unauthorized() -> Response:
    output = {"error":
                  {"msg": "401 error: The email or password provided is invalid."}
              }
    resp = jsonify({'result': output})
    resp.status_code = 401
    return resp


def forbidden() -> Response:
    output = {"error":
                  {"msg": "403 error: The current user is not authorized to take this action."}
              }
    resp = jsonify({'result': output})
    resp.status_code = 403
    return resp


def invalid_route() -> Response:
    output = {"error":
                  {"msg": "404 error: This route is currently not supported. See API documentation."}
              }
    resp = jsonify({'result': output})
    resp.status_code = 404
    return resp


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        user = User.objects(email=data.get('email')).get()
        auth_success = user.check_pwd(data.get('password'))
        if not auth_success:
            return unauthorized()
        expiry = datetime.timedelta(days=5)
        access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify({'result': {'access_token': access_token,
                                   'refresh_token': refresh_token,
                                   'logged_in_as': f"{user.email}"}})
    except DoesNotExist:
        print("USER NOT FOUND")


@app.route("/professores", methods=['POST'])
def store():
    request_data = request.get_json()
    schema = {
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'name': {'type': 'string'}
    }
    v = Validator(schema)
    if not v.validate(request_data):
        return jsonify(erro="dados invalidos"), 400
    print(v.validate(request_data))
    professor = User.from_json(json.dumps(request_data))
    professor.save()
    return jsonify(professor), 200


@app.route('/required')
@jwt_required
def test():
    return "TANTANTAAAAAN"
