from cerberus import Validator
from flask import request, jsonify
from datetime import datetime

from flask_jwt_extended import jwt_required
from mongoengine import OperationError

from src.models.Bibliografia import Bibliografia
from src.models.Disciplina import Disciplina, Ementa
from src.services.BibliografiaService import BibliografiaService
from src.services.DisciplinaService import DisciplinaService


def return_not_found():
    output = {"error": {"msg": "500 error: Disciplina não encontrada."}}
    resp = jsonify({'result': output})
    resp.status_code = 500
    return resp


def validate_all(data):
    v = Validator()
    v.schema = {
        'nome': {'required': True, 'type': 'string'},
        'pratica': {'required': True, 'type': 'integer', 'allowed': [0, 20, 40, 80]},
        'teoria': {'required': True, 'type': 'integer', 'allowed': [0, 20, 40, 80]},
        'semestre': {'required': True, 'type': 'integer'},
        'ementa': {'required': True, 'type': 'dict', 'schema': {
            'descricao': {'type': 'string'},
            'conteudo': {'type': ['string', 'list']},
            'competencias': {'type': ['string', 'list']},
            'objetivos': {'type': ['string', 'list']},
        }},
        'basica': {'type': ['string', 'list']},
        'complementar': {'type': ['string', 'list']}
    }
    if not v.validate(data):
        return jsonify(error=v.errors), 400


class DisciplinaController:
    @staticmethod
    def index_disciplina():
        disciplinas: [Disciplina] = DisciplinaService.get_all_as_dict()

        return jsonify(disciplinas)

    @staticmethod
    @jwt_required
    def store_disciplina():
        data = request.get_json()
        validate_all(data)

        disciplina = Disciplina()
        disciplina.nome = data.get('nome')
        disciplina.carga_pratica = data.get('pratica')
        disciplina.carga_teoria = data.get('teoria')
        disciplina.semestre = data.get('semestre')

        # region EMENTA
        ementa = Ementa()
        ementa.data = datetime.utcnow()
        ementa.descricao = data.get('ementa')['descricao']
        ementa.conteudo = data.get('ementa')['conteudo']
        ementa.competencias = data.get('ementa')['competencias']
        ementa.objetivos = data.get('ementa')['objetivos']

        for lib_id in data.get('basica'):
            bibliografia: Bibliografia = BibliografiaService.get_by_id(lib_id)
            ementa.bibliografia_basica.append(bibliografia)
        for lib_id in data.get('complementar'):
            bibliografia: Bibliografia = BibliografiaService.get_by_id(lib_id)
            ementa.bibliografia_complementar.append(bibliografia)
        disciplina.ementas.append(ementa)
        # endregion

        disciplina.save()
        return jsonify(disciplina)

    @staticmethod
    @jwt_required
    def show_disciplina(id):
        disciplina: Disciplina = DisciplinaService.get_by_id(id)
        if disciplina is None:
            return_not_found()
        return jsonify(disciplina.to_dict())

    @staticmethod
    @jwt_required
    def new_ementa():
        id_disc = request.headers.get('id_disc')
        data = request.get_json()

        disciplina: Disciplina = DisciplinaService.get_by_id(id_disc)
        if disciplina is None:
            return_not_found()

        ementa = Ementa()
        ementa.data = datetime.utcnow()
        ementa.descricao = data.get('descricao')
        ementa.conteudo = data.get('conteudo')
        ementa.competencias = data.get('competencias')
        ementa.objetivos = data.get('objetivos')
        ementa.bibliografia_basica = DisciplinaService.add_bibliografia_to_ementa(data.get('basica'))
        ementa.bibliografia_complementar = DisciplinaService.add_bibliografia_to_ementa(data.get('complementar'))
        # disciplina.ementas.append(ementa)
        ementas: [Ementa] = disciplina.ementas
        ementas.append(ementa)
        disciplina.ementas = ementas
        disciplina.save()
        return jsonify(disciplina.to_dict())

    @staticmethod
    @jwt_required
    def update_disciplina(id):
        data = request.get_json()
        validate_all(data)
        print('teste')
        disciplina: Disciplina = DisciplinaService.get_by_id(id)
        if disciplina is None:
            return_not_found()

        disciplina.nome = data.get('nome')
        disciplina.carga_pratica = data.get('pratica')
        disciplina.carga_teoria = data.get('teoria')
        disciplina.semestre = data.get('semestre')
        ementa = Ementa()
        ementa.data = datetime.utcnow()
        ementa.descricao = data.get('ementa')['descricao']
        ementa.conteudo = data.get('ementa')['conteudo']
        ementa.competencias = data.get('ementa')['competencias']
        ementa.objetivos = data.get('ementa')['objetivos']
        ementa.bibliografia_basica = DisciplinaService.add_bibliografia_to_ementa(data.get('basica'))
        ementa.bibliografia_complementar = DisciplinaService.add_bibliografia_to_ementa(data.get('complementar'))
        disciplina.ementas[0] = ementa

        disciplina.save()
        return jsonify(disciplina.to_dict())

    @staticmethod
    @jwt_required
    def destroy_disciplina(id):
        disciplina: Disciplina = DisciplinaService.get_by_id(id)

        if disciplina is None:
            return_not_found()

        try:
            disciplina.delete()
            return jsonify(), 200
        except OperationError:
            return jsonify(OperationError)
