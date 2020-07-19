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
    curso: Curso
    for curso in cursos:
        curso_list.append(curso.to_dict_first_grade())

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
    curso: Curso = CursoService.get_curso_by_id(id)
    if curso is None:
        output = {"error": {"msg": "500 error: Curso not found."}}
        resp = jsonify({'result': output})
        resp.status_code = 500
        return resp

    return jsonify(curso.to_dict_first_grade())


@jwt_required
def update_curso(id):
    data = request.get_json()
    validate_all(data)

    curso: Curso = CursoService.get_curso_by_id(id)
    if curso is None:
        return_curso_not_found()

    coordenador = UserService.get_by_id(data.get('user_id'))
    if coordenador is None:
        return_user_not_found()

    curso.nome = data.get('nome')
    curso.turno = data.get('turno')
    curso.coordenador = coordenador

    grade: Grade = set_grade_from_data(data.get('grade'))
    curso.grades[0] = grade
    curso.save()

    return jsonify(curso.to_dict())


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


def return_curso_not_found():
    output = {"error": {"msg": "500 error: Curso não encontrado."}}
    resp: object = jsonify({'result': output})
    resp.status_code = 500
    return resp


def set_grade_from_data(data):
    grade = Grade()
    grade.ano = data['ano']
    for disc_id in data['disciplinas']:
        disc: Disciplina = DisciplinaService.get_by_id(disc_id)
        grade.disciplinas.append(disc)
    return grade
