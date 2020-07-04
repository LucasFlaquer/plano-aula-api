from cerberus import Validator
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from mongoengine import OperationError, NotUniqueError

from src.models.Bibliografia import Bibliografia
from src.services.BibliografiaService import BibliografiaService


def return_not_found():
    output = {"error": {"msg": "500 error: Bibliografia não encontrada."}}
    resp = jsonify({'result': output})
    resp.status_code = 500
    return resp


def validate(data):
    v = Validator()
    v.schema = {
        'nome': {'required': True, 'type': 'string'},
        'autor': {'required': False, 'type': 'string'},
        'editora': {'required': False, 'type': 'string'}
    }

    if not v.validate(data):
        return jsonify(error=v.errors), 400


class BibliografiaController:
    @staticmethod
    @jwt_required
    def index_bibliografia():
        bibliografias: [Bibliografia] = BibliografiaService.get_all_as_dict()
        return jsonify(bibliografias)

    @staticmethod
    @jwt_required
    def store_bibliografia():
        data = request.get_json()
        validate(data)
        try:
            bibliografia = Bibliografia()
            bibliografia.nome = data.get('nome')
            bibliografia.autor = data.get('autor')
            bibliografia.editora = data.get('editora')
            bibliografia.save()
        except NotUniqueError:
            return jsonify(
                error="O campo Nome deve ser único"
            ), 422
        return jsonify(bibliografia.to_dict())

    @staticmethod
    @jwt_required
    def show_bibliografia(id):
        bibliografia = BibliografiaService.get_by_id(id)
        if bibliografia is None:
            return_not_found()
        return jsonify(bibliografia.to_dict())

    @staticmethod
    @jwt_required
    def update_bibliografia(id):
        data = request.get_json()
        bibliografia: Bibliografia = BibliografiaService.get_by_id(id)
        if bibliografia is None:
            return_not_found()

        bibliografia.nome = data.get('nome')
        bibliografia.autor = data.get('autor') if data.get('autor') else bibliografia.autor
        bibliografia.editora = data.get('editora') if data.get('editora') else bibliografia.editora
        bibliografia.save()

        return jsonify(bibliografia.to_dict())

    @staticmethod
    @jwt_required
    def delete_bibliografia(id):
        bibliografia: Bibliografia = BibliografiaService.get_by_id(id)
        if bibliografia is None:
            return_not_found()

        try:
            bibliografia.delete()
            return jsonify(), 200
        except OperationError:
            return jsonify(OperationError)
