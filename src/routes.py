import datetime

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from mongoengine import DoesNotExist

from src import app
from src.controllers.BibliografiaController import BibliografiaController
from src.controllers.CursoController import CursoController
from src.controllers.DisciplinaController import DisciplinaController
from src.controllers.UserController import UserController
from src.functions.errors import unauthorized
from src.models.User import User

userController = UserController()
cursoController = CursoController()
disciplinaController = DisciplinaController()


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
app.add_url_rule('/users', view_func=userController.index, methods=['GET'])
app.add_url_rule('/users', view_func=userController.store, methods=['POST'])
app.add_url_rule('/users/<id>', view_func=userController.show, methods=['GET'])
app.add_url_rule('/users/me', view_func=userController.loggedUser, methods=['GET'])
app.add_url_rule('/users/update', view_func=userController.update, methods=['PUT'])
app.add_url_rule('/users/<id>', view_func=userController.destroy, methods=['DELETE'])

# region CRUD DE DISCIPLINAS
app.add_url_rule('/disciplinas', view_func=DisciplinaController.index_disciplina, methods=['GET'])
app.add_url_rule('/disciplinas', view_func=DisciplinaController.store_disciplina, methods=['POST'])
app.add_url_rule('/disciplinas/<id>', view_func=DisciplinaController.show_disciplina, methods=['GET'])
app.add_url_rule('/disciplinas/<id>', view_func=DisciplinaController.update_disciplina, methods=['PUT'])
app.add_url_rule('/disciplinas/ementa', view_func=DisciplinaController.new_ementa, methods=['PATCH'])
# endregion

# # CRUD DE CURSORS
app.add_url_rule('/cursos', view_func=cursoController.indexCursos, methods=['GET'])
app.add_url_rule('/cursos', view_func=cursoController.storeCurso, methods=['POST'])
app.add_url_rule('/cursos/<id>', view_func=cursoController.showCurso, methods=['GET'])
app.add_url_rule('/cursos/<id>', view_func=cursoController.updateCurso, methods=['PUT'])
app.add_url_rule('/cursos/<id>', view_func=cursoController.deleteCurso, methods=['DELETE'])

# region BIBLIOGRAFIAS
app.add_url_rule('/bibliografias', view_func=BibliografiaController.index_bibliografia, methods=['GET'])
app.add_url_rule('/bibliografias', view_func=BibliografiaController.store_bibliografia, methods=['POST'])
app.add_url_rule('/bibliografias/<id>', view_func=BibliografiaController.show_bibliografia, methods=['GET'])
app.add_url_rule('/bibliografias/<id>', view_func=BibliografiaController.update_bibliografia, methods=['PUT'])
app.add_url_rule('/bibliografias/<id>', view_func=BibliografiaController.destroy_bibliografia, methods=['DELETE'])

# endregion


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
