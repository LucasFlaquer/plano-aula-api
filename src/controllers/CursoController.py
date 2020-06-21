from flask import request, jsonify

from src.models.Curso import Curso
from src.services.UserService import UserService


class CursoController:


    @staticmethod
    def store():
        data = request.get_json()
        print('--------------addCurso')
        # coordenador = UserService.getUserById(data.get('user_id'))
        # curso=Curso()
        # curso.nome=data.get('nome')
        # curso.turno=data.get('turno')
        # curso.coordenador=coordenador
        # print(curso.turno)

        return jsonify(ok=True)

