import datetime

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from mongoengine import DoesNotExist

from src import app
from src.controllers.CursoController import CursoController
from src.controllers.UserController import UserController
from src.functions.errors import unauthorized
from src.models.User import User

userController = UserController()
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
        #                'refresh_token': refresh_token,
        #                'logged_in_as': f"{user.email}"},
        #     'name': f"{user.name}"
        # })
    except DoesNotExist:
        print("USER NOT FOUND")
        return jsonify(error="USER NOT FOUND"), 500


# rotas de usuario
app.add_url_rule('/users', view_func=userController.index, methods=['GET'])
app.add_url_rule('/users', view_func=userController.store, methods=['POST'])
app.add_url_rule('/users/<id>', view_func=userController.show, methods=['GET'])
app.add_url_rule('/users/me', view_func=userController.loggedUser, methods=['GET'])
app.add_url_rule('/users/update', view_func=userController.update, methods=['PUT'])
app.add_url_rule('/users/<id>', view_func=userController.destroy, methods=['DELETE'])

# # CRUD DE CURSORS
app.add_url_rule('/cursos', view_func=cursoController.indexCursos, methods=['GET'])
app.add_url_rule('/cursos', view_func=cursoController.storeCurso, methods=['POST'])
app.add_url_rule('/cursos/<id>', view_func=CursoController.showCurso, methods=['GET'])
app.add_url_rule('/curos/<id>', view_func=CursoController.updateCurso, methods=['PUT'])
app.add_url_rule('/cursos/<id>', view_func=CursoController.deleteCurso, methods=['DELETE'])

'''
    ROTAS:
        cadastrar usuario
        editar usuario (outro)
        listar todos os usuários
        editar usuario logado (me)
        exibir informacoes do usuario logado (me)
        deletar usuário
        login/logout
               
        cadastrar cursos
        editar coordenador
        editar curso
        exibir informacoes do curso
        exibir disciplinas do curso
        alterar disciplinas do curso
        
        cadastrar disciplina
        listar todas as disciplinas
        cadastrar ementa para a disciplina
        
        
'''
