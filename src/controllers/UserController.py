import json

from cerberus import Validator
from flask import jsonify, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import DoesNotExist, ValidationError, errors

from src.functions.errors import forbidden
from src.models.User import User
from src.services.DisciplinaService import DisciplinaService
from src.services.UserService import UserService


def validate_disciplinas_path(data):
    v = Validator()
    v.schema = {
        'disc_ids': {'required': True, 'type': ['string', 'list']}
    }
    if not v.validate(data):
        return jsonify(error=v.errors), 400


@jwt_required
def index():
    users = UserService.get_all_as_dict()
    return jsonify(users)


# @jwt_required
def store():
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

    if request_data.get('access') is None:
        user = User()
        user.email = request_data.get('email')
        user.password = request_data.get('password')
        user.name = request_data.get('name')
    else:
        user = User.from_json(json.dumps(request_data))
    user.save()
    return jsonify(user.to_dict()), 200


@jwt_required
def show(self, id):
    user = self.service.get_by_id(id)
    if user is None:
        output = {"error": {"msg": "500 error: User not found."}}
        resp = jsonify({'result': output})
        resp.status_code = 500
        return resp
    return jsonify(user)


@jwt_required
def loggedUser():
    user = User.objects(id=get_jwt_identity()).get()
    print(user)
    return jsonify(user.to_dict())


# @jwt_required
def update():
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


def updateUserAccess():
    request_data = request.get_json()
    schema = {
        'user_id': {'type': 'string'},
        'access': {'required': False, 'type': ['string', 'list']}
    }
    v = Validator(schema)
    if not v.validate(request_data):
        return jsonify(
            erro="dados invalidos",
            message=v.errors
        ), 400

    user = UserService.get_by_id(id=request_data.get('user_id'))
    if user is None:
        output = {"error": {"msg": "500 error: User not found."}}
        resp = jsonify({'result': output})
        resp.status_code = 500
        return resp

    print(request_data.get('access'))


@jwt_required
def destroy():
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


@jwt_required
def update_disciplinas():
    data = request.get_json()
    id_user = request.headers.get('id_user')
    validate_disciplinas_path(data)
    user: User = UserService.get_by_id(id_user)
    if user is None:
        return_not_found()

    disciplinas = []
    for disc_id in data.get('disc_ids'):
        disc = DisciplinaService.get_by_id(disc_id)
        disciplinas.append(disc)

    user.disciplinas_ministradas = disciplinas
    user.save()
    return jsonify(user.to_dict())


def return_not_found():
    output = {"error": {"msg": "500 error: User not found."}}
    resp = jsonify({'result': output})
    resp.status_code = 500
    return resp
