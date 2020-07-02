import json
from typing import Optional, Any

from cerberus import Validator
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from src.models.Curso import Curso
from src.services.CursoService import CursoService
from src.services.UserService import UserService
from mongoengine import *


class CursoController:

    @jwt_required
    def indexCursos(self):
        cursos = CursoService.get_all()
        cursoList = []
        for curso in cursos:

            if not curso.coordenador:
                coord = None
            else:
                coord = dict(id=str(curso.coordenador.pk), nome=curso.coordenador.name)

            d_curso = dict(
                id=str(curso.pk),
                nome=curso.nome,
                turno=curso.turno,
                coordenador=coord
            )
            cursoList.append(d_curso)

        return jsonify(cursoList)

    @jwt_required
    def storeCurso(self):
        data = request.get_json()
        schema = {
            'nome': {'required': True, 'type': 'string'},
            'turno': {'type': 'string'},
            'user_id': {'type': 'string', 'required': False},
            'disciplinas': {'type': ['string', 'list']}
        }
        v = Validator(schema)
        if not v.validate(data):
            return jsonify(
                erro="dados invalidos",
                message=v.errors
            ), 400

        curso = Curso()
        curso.nome = data.get('nome')
        curso.turno = data.get('turno')

        if data.get('user_id'):
            coordenador = UserService.getUserById(data.get('user_id'))

            if coordenador is None:
                output = {"error": {"msg": "500 error: Professor not found."}}
                resp = jsonify({'result': output})
                resp.status_code = 500
                return resp
            else:
                curso.coordenador = coordenador

        # for disc_id in data.get('disciplinas'):
        #           disc = DiscService.getDiscById(disc_id)
        #       ....

        curso.save()
        if not curso.coordenador:
            coord = None
        else:
            coord = dict(id=str(curso.coordenador.pk), nome=curso.coordenador.name)

        d_curso = dict(
            id=str(curso.pk),
            nome=curso.nome,
            turno=curso.turno,
            coordenador=coord
        )
        return jsonify(d_curso)

    @jwt_required
    def showCurso(self, id):
        curso = CursoService.get_curso_by_id(id=id)
        if curso is None:
            output = {"error": {"msg": "500 error: Curso not found."}}
            resp = jsonify({'result': output})
            resp.status_code = 500
            return resp

        return curso

    @jwt_required
    def updateCurso(self, id):
        print('-------estou aqui')
        print(id)
        request_data = request.get_json()
        schema = {
            'nome': {'type': 'string'},
            'turno': {'type': 'string'},
            'user_id': {'type': 'string'}
        }
        v = Validator(schema)
        if not v.validate(request_data):
            return jsonify(erro="dados invalidos"), 400

        curso: Curso = CursoService.get_curso_by_id(id=id)
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
        if not curso.coordenador:
            coord = None
        else:
            coord = dict(id=str(curso.coordenador.pk), nome=curso.coordenador.name)

        d_curso = dict(
            id=str(curso.pk),
            nome=curso.nome,
            turno=curso.turno,
            coordenador=coord
        )
        return jsonify(d_curso)

    @staticmethod
    def deleteCurso(id):
        curso: Curso = CursoService.get_curso_by_id(id)
        if curso is None:
            output = {"error": {"msg": "500 error: Curso not found."}}
            resp = jsonify({'result': output})
            resp.status_code = 500
            return resp

        curso.delete()
        return jsonify(), 200
