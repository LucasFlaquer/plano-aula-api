import datetime
import json
from cerberus import Validator
from flask import request, Response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from mongoengine import DoesNotExist

from src import app
from src.controllers.UserController import UserController
from src.functions.errors import unauthorized
from src.models.User import User


userControler = UserController()


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


# @jwt_required
app.add_url_rule('/users', view_func=userControler.index, methods=['GET'])
app.add_url_rule('/users', view_func=userControler.store, methods=['POST'])
app.add_url_rule('/users/<id>', view_func=userControler.show, methods=['GET'])
app.add_url_rule('/users/me', view_func=userControler.loggedUser, methods=['GET'])
#update de usuario logado
app.add_url_rule('/users/update', view_func=userControler.update, methods=['PUT'])
app.add_url_rule('/users/<id>', view_func=userControler.destroy, methods=['DELETE'])

# @app.route("/professores", methods=['POST'])
# def store():
#     request_data = request.get_json()
#     schema = {
#         'email': {'type': 'string'},
#         'password': {'type': 'string'},
#         'name': {'type': 'string'}
#     }
#     v = Validator(schema)
#     if not v.validate(request_data):
#         return jsonify(erro="dados invalidos"), 400
#     print(v.validate(request_data))
#     professor = User.from_json(json.dumps(request_data))
#     professor.save()
#     return jsonify(professor), 200
#
#
# @app.route('/required')
# @jwt_required
# def test():
#     return "TANTANTAAAAAN"
