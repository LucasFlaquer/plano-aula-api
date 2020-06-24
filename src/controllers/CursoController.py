from typing import Optional, Any

from cerberus import Validator
from flask import request, jsonify

from src.models.Curso import Curso
from src.services.CursoService import CursoService
from src.services.UserService import UserService
from mongoengine import *

class CursoController:

    def listAllCursos(self):
        cursos = CursoService.getAll()
        return jsonify(cursos)

    @staticmethod
    def store_curso():
        data = request.get_json()

        coordenador = UserService.getUserById(data.get('user_id'))
        if coordenador is None:
            output = {"error": {"msg": "500 error: Professor not found."}}
            resp = jsonify({'result': output})
            resp.status_code = 500
            return resp

        curso = Curso()
        curso.nome = data.get('nome')
        curso.turno = data.get('turno')
        curso.coordenador = coordenador
        curso.save()
        return jsonify(curso)

    @staticmethod
    def show_curso(id):
        curso = CursoService.getCursoById(id=id)
        if curso is None:
            output = {"error": {"msg": "500 error: Curso not found."}}
            resp = jsonify({'result': output})
            resp.status_code = 500
            return resp

        return curso

    @staticmethod
    def update_curso(id):
        request_data = request.get_json()
        schema = {
            'nome': {'type': 'string'},
            'turno': {'type': 'string'},
            'user_id': {'type': 'string'}
        }
        v = Validator(schema)
        if not v.validate(request_data):
            return jsonify(erro="dados invalidos"), 400

        curso: Curso = CursoService.getCursoById(id)
        if curso is None:
            output = {"error": {"msg": "500 error: Curso not found."}}
            resp = jsonify({'result': output})
            resp.status_code = 500
            return resp

        coordenador = UserService.getUserById(request_data.get('user_id'))
        if coordenador is None:
            output = {"error": {"msg": "500 error: Professor not found."}}
            resp = jsonify({'result': output})
            resp.status_code = 500
            return resp

        curso.nome = request_data.get('nome')
        curso.turno = request_data.get('turno')
        curso.coordenador = coordenador
        curso.save()

        return jsonify(curso)

    @staticmethod
    def delete_curso(id):
        curso: Curso = CursoService.getCursoById(id)
        if curso is None:
            output = {"error": {"msg": "500 error: Curso not found."}}
            resp = jsonify({'result': output})
            resp.status_code = 500
            return resp

        curso.delete()
        return jsonify(), 200