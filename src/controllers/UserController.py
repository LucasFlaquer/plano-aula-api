import json

from cerberus import Validator
from flask import jsonify, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import DoesNotExist, ValidationError, errors

from src.functions.errors import forbidden
from src.models.User import User


class UserController:
    @jwt_required
    def index(self):
        # Listar todos os usuarios
        users = User.objects()
        return jsonify(users)

    @jwt_required
    def store(self):
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
        user = User.from_json(json.dumps(request_data))
        user.save()
        return jsonify(user), 200

    @jwt_required
    def show(self, id):
        try:
            user = User.objects(id=id).get()
            return jsonify(user)
        except (User.DoesNotExist, ValidationError):
            output = {"error":
                          {"msg": "500 error: User not found."}
                      }
            resp = jsonify({'result': output})
            resp.status_code = 500
            return resp

    @jwt_required
    def loggedUser(self):
        user = User.objects(id=get_jwt_identity()).get()
        return jsonify(user)

    @jwt_required
    def update(self):
        request_data = request.get_json()
        schema = {
            'email': {'type': 'string'},
            'password': {'type': 'string'}
        }
        v = Validator(schema)
        if not v.validate(request_data):
            return jsonify(erro="dados invalidos"), 400

        try:
            user = User.objects(id=get_jwt_identity()).get()
            print(user.email)
            user.email = request_data.get('email')
            user.password = request_data.get('password')
            user.save()
            return jsonify(user)

        except:
            return forbidden()

    @jwt_required
    def destroy(self):
        try:
            user = User.objects(id=id).get()
            return jsonify(), 200
        except (User.DoesNotExist, ValidationError):
            output = {"error":
                          {"msg": "500 error: User not found."}
                      }
            resp = jsonify({'result': output})
            resp.status_code = 500
            return resp