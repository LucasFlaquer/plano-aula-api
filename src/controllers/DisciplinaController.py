from cerberus import Validator
from flask import request, jsonify
from datetime import datetime

from flask_jwt_extended import jwt_required

from src.models.Bibliografia import Bibliografia
from src.models.Disciplina import Disciplina, Ementa
from src.services.BibliografiaService import BibliografiaService
from src.services.DisciplinaService import DisciplinaService


class DisciplinaController:
    @staticmethod
    def index_disciplina():
        disciplinas: [Disciplina] = DisciplinaService.get_all_as_dict()

        return jsonify(disciplinas)

    @staticmethod
    @jwt_required
    def store_disciplina():
        data = request.get_json()
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
            print(v.errors)
            return jsonify(errors=v.errors), 400

        disciplina = Disciplina()
        disciplina.nome = data.get('nome')
        disciplina.carga_pratica = data.get('pratica')
        disciplina.carga_teoria = data.get('teoria')
        disciplina.semestre = data.get('semestre')

        # region EMENTA
        ementa = Ementa()
        ementa.data = datetime.strptime('18/09/19 01:55:19', '%d/%m/%y %H:%M:%S')
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

    # @staticmethod
    # def show_disciplina(id):
    #     disciplina: Disciplina = DisciplinaService.get_disc_by_id(id)
    #
    #     if disciplina is None:
    #         output = {"error": {"msg": "500 error: Disciplina não encontrada."}}
    #         resp = jsonify({'result': output})
    #         resp.status_code = 500
    #         return resp
    #
    #     return jsonify(disciplina.to_dict())
    #
    # def update_disciplina(self, id):
    #     data = request.get_json()
    #     # atualizar a disciplina
    #
    # def nova_ementa(self, id):
    #     data = request.get_json()
    #
    # def update_ementa(self, id):
    #     data = request.get_json()
