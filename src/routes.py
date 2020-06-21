import datetime
from flask import request, Response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from mongoengine import DoesNotExist

from src import app
from src.controllers.CursoController import CursoController
from src.controllers.UserController import UserController
from src.functions.errors import unauthorized
from src.models.User import User


userControler = UserController()
cursoController = CursoController()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        user = User.objects(email=data.get('email')).get()
        auth_success = user.check_pwd(data.get('password'))
        if not auth_success:
            return unauthorized()
        expiry = datetime.timedelta(minutes=5)
        access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify(
            access_token=access_token,
            logged_in_as=user.email,
            name=user.name
        )
        # return jsonify({
        #     'result': {'access_token': access_token,
        #                            'refresh_token': refresh_token,
        #                            'logged_in_as': f"{user.email}"},
        #                            'name':f"{user.name}"
        #                            })
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


########## CRUD DE CURSOS ################
app.add_url_rule('/cursos', view_func=CursoController.store, methods=['POST'])

# @app.route('/cursos', methods=['POST'])
# def addCurso():
#     data = request.get_json()
#     print(data)
#     curso = Curso
#     print(curso.nome)
#     print(curso.coordenador)
#     return jsonify(ok=True)
