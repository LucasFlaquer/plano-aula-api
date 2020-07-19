import datetime

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from mongoengine import DoesNotExist

from src import app
from src.controllers import BibliografiaController, UserController
from src.controllers import CursoController
from src.controllers import DisciplinaController
from src.functions.errors import unauthorized
from src.models.User import User


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        user = User.objects(email=data.get('email')).get()
        auth_success = user.check_pwd(data.get('password'))
        if not auth_success:
            return unauthorized()
        expiry = datetime.timedelta(hours=2)
        access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify(
            access_token=access_token,
            logged_in_as=user.email,
            name=user.name
        )
        # return jsonify({
        #     'result': {'access_token': access_token,
        #                'refresh_token': refresh_token,
        #                'logged_in_as': f"{user.email}"},
        #     'name': f"{user.name}"
        # })
    except DoesNotExist:
        print("USER NOT FOUND")
        return jsonify(error="USER NOT FOUND"), 500


# rotas de usuario
app.add_url_rule('/users', view_func=UserController.index, methods=['GET'])
app.add_url_rule('/users', view_func=UserController.store, methods=['POST'])
app.add_url_rule('/users/<id>', view_func=UserController.show, methods=['GET'])
app.add_url_rule('/users/me', view_func=UserController.loggedUser, methods=['GET'])
app.add_url_rule('/users/update', view_func=UserController.update, methods=['PUT'])
app.add_url_rule('/users/<id>', view_func=UserController.destroy, methods=['DELETE'])

# region BIBLIOGRAFIAS
app.add_url_rule('/bibliografias', view_func=BibliografiaController.index_bibliografia, methods=['GET'])
app.add_url_rule('/bibliografias', view_func=BibliografiaController.store_bibliografia, methods=['POST'])
app.add_url_rule('/bibliografias/<id>', view_func=BibliografiaController.show_bibliografia, methods=['GET'])
app.add_url_rule('/bibliografias/<id>', view_func=BibliografiaController.update_bibliografia, methods=['PUT'])
app.add_url_rule('/bibliografias/<id>', view_func=BibliografiaController.destroy_bibliografia, methods=['DELETE'])

# endregion

# region CRUD DE DISCIPLINAS
app.add_url_rule('/disciplinas', view_func=DisciplinaController.index_disciplina, methods=['GET'])
app.add_url_rule('/disciplinas', view_func=DisciplinaController.store_disciplina, methods=['POST'])
app.add_url_rule('/disciplinas/<id>', view_func=DisciplinaController.show_disciplina, methods=['GET'])
app.add_url_rule('/disciplinas/<id>', view_func=DisciplinaController.update_disciplina, methods=['PUT'])
app.add_url_rule('/disciplinas/ementa', view_func=DisciplinaController.new_ementa, methods=['PATCH'])
# endregion

# # CRUD DE CURSORS
app.add_url_rule('/cursos', view_func=CursoController.index_curso, methods=['GET'])
app.add_url_rule('/cursos', view_func=CursoController.store_curso, methods=['POST'])
app.add_url_rule('/cursos/<id>', view_func=CursoController.show_curso, methods=['GET'])
app.add_url_rule('/cursos/<id>', view_func=CursoController.update_curso, methods=['PUT'])
app.add_url_rule('/cursos/<id>', view_func=CursoController.delete_curso, methods=['DELETE'])
