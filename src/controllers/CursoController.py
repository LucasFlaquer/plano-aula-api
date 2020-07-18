import json
from typing import Optional, Any

from cerberus import Validator
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from src.models.Curso import Curso, Grade
from src.models.Disciplina import Disciplina
from src.services.CursoService import CursoService
from src.services.DisciplinaService import DisciplinaService
from src.services.UserService import UserService
from mongoengine import *


@jwt_required
def index_curso():
    cursos = CursoService.get_all()
    curso_list = []
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
        curso_list.append(d_curso)

    return jsonify(curso_list)


@jwt_required
def store_curso():
    data = request.get_json()
    validate_all(data)

    curso = Curso()
    curso.nome = data.get('nome')
    coordenador = UserService.get_by_id(data.get('user_id'))
    if coordenador is None:
        return_user_not_found()

    curso.coordenador = coordenador
    grade = Grade()
    grade.ano = data.get('grade')['ano']
    for disc_id in data.get('grade')['disciplinas']:
        disc: Disciplina = DisciplinaService.get_by_id(disc_id)
        grade.disciplinas.append(disc)

    curso.grades.append(grade)
    curso.save()
    return jsonify(curso.to_dict())


@jwt_required
def show_curso(id):
    curso = CursoService.get_curso_by_id(id=id)
    if curso is None:
        output = {"error": {"msg": "500 error: Curso not found."}}
        resp = jsonify({'result': output})
        resp.status_code = 500
        return resp

    return curso


# @jwt_required
# def update_curso(id):
#     request_data = request.get_json()
#     schema = {
#         'nome': {'type': 'string'},
#         'turno': {'type': 'string'},
#         'user_id': {'type': 'string'}
#     }
#     v = Validator(schema)
#     if not v.validate(request_data):
#         return jsonify(erro="dados invalidos"), 400
#
#     curso: Curso = CursoService.get_curso_by_id(id=id)
#     if curso is None:
#         output = {"error": {"msg": "500 error: Curso not found."}}
#         resp = jsonify({'result': output})
#         resp.status_code = 500
#         return resp
#
#     coordenador = UserService.getUserById(request_data.get('user_id'))
#     if coordenador is None:
#         output = {"error": {"msg": "500 error: Professor not found."}}
#         resp = jsonify({'result': output})
#         resp.status_code = 500
#         return resp
#
#     curso.nome = request_data.get('nome')
#     curso.turno = request_data.get('turno')
#     curso.coordenador = coordenador
#     curso.save()
#     if not curso.coordenador:
#         coord = None
#     else:
#         coord = dict(id=str(curso.coordenador.pk), nome=curso.coordenador.name)
#
#     d_curso = dict(
#         id=str(curso.pk),
#         nome=curso.nome,
#         turno=curso.turno,
#         coordenador=coord
#     )
#     return jsonify(d_curso)
#

def delete_curso(id):
    curso: Curso = CursoService.get_curso_by_id(id)
    if curso is None:
        output = {"error": {"msg": "500 error: Curso not found."}}
        resp = jsonify({'result': output})
        resp.status_code = 500
        return resp

    curso.delete()
    return jsonify(), 200


def validate_all(data):
    schema = {
        'nome': {'required': True, 'type': 'string'},
        'user_id': {'type': 'string', 'required': True},
        'ano': {'type': 'integer', 'required': True},
        'grade': {'type': 'dict', 'schema': {
            'ano': {'type': 'integer'},
            'disciplinas': {'type': ['string', 'list']}
        }}

    }
    v = Validator(schema)
    if not v.validate(data):
        return jsonify(
            erro="dados invalidos",
            message=v.errors
        ), 400


def return_user_not_found():
    output = {"error": {"msg": "500 error: Professor não encontrado."}}
    resp: object = jsonify({'result': output})
    resp.status_code = 500
    return resp
