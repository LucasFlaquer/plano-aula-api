import json

from cerberus import Validator
from flask import jsonify, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import DoesNotExist, ValidationError, errors

from src.functions.errors import forbidden
from src.models.User import User
from src.services.UserService import UserService


class UserController:

    service = UserService

    def index(self):
        # Listar todos os usuarios
        users = User.objects()
        return jsonify(users)


    def store(self):
        request_data = request.get_json()
        schema = {
            'email': {'type': 'string'},
            'password': {'type': 'string'},
            'name': {'type': 'string'},
            'access': {'required': False, 'type': 'dict', 'schema': {
                'admin': {'type': 'boolean'},
                'nde': {'type': 'boolean'},
                'coordenador': {'type': 'boolean'},
                'qualidade': {'type': 'boolean'}
            }}
        }
        v = Validator(schema)
        if not v.validate(request_data):
            return jsonify(
                erro="dados invalidos",
                message=v.errors
            ), 400

        # user = User.from_json(json.dumps(request_data))
        # print(User.access.admin)


        if request_data.get('access') is None:
            user = User()
            user.email = request_data.get('email')
            user.password = request_data.get('password')
            user.name = request_data.get('name')
        else:
            user = User.from_json(json.dumps(request_data))

        user.save()

        return jsonify(user), 200

    #@jwt_required
    #@staticmethod
    def show(self, id):
        user = self.service.getUserById(id)
        if user is None:
            output = {"error": {"msg": "500 error: User not found."} }
            resp = jsonify({'result': output})
            resp.status_code = 500
            return resp
        return jsonify(user)

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