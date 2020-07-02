from cerberus import Validator
from flask import request, jsonify
from datetime import datetime

from src.models.Disciplina import Disciplina, Ementa
from src.services.DisciplinaService import DisciplinaService


class DisciplinaController:
    @staticmethod
    def index_disciplina():
        disciplinas: [Disciplina] = DisciplinaService.get_all()

        return disciplinas

    def store_disciplina(self):
        data = request.get_json()
        v = Validator()
        v.schema = {
            'nome': {'required': True, 'type': 'string'},
            'pratica': {'required': True, 'type': 'integer', 'allowed': [0, 40, 80]},
            'teoria': {'required': True, 'type': 'integer', 'allowed': [0, 40, 80]},
            'ementa': {'required': True, 'type': 'dict', 'schema': {
                'ementa': {'type': 'string'},
                'conteudo': {'type': ['string', 'list']},
                'competencias': {'type': ['string', 'list']},
                'objetivos': {'type': ['string', 'list']},
            }}
        }

        if not v.validate(data):
            print(v.errors)
            return jsonify(errors=v.errors), 400

        disciplina = Disciplina()
        disciplina.nome = data.get('nome')

        pratica = data.get('pratica')
        teorica = data.get('teoria')
        soma = pratica + teorica
        if soma > 80 or soma < 40:
            return jsonify(error="ERRO 500: A relacao de aulas teorica e prática inválida"), 500
        disciplina.carga_pratica = data.get('pratica')
        disciplina.carga_teoria = data.get('teoria')

        ementa = Ementa()
        ementa.data = datetime.strptime('18/09/19 01:55:19', '%d/%m/%y %H:%M:%S')
        ementa.ementa = data.get('ementa')['ementa']
        ementa.conteudo = data.get('ementa')['conteudo']
        ementa.competencias = data.get('ementa')['competencias']
        ementa.objetivos = data.get('ementa')['objetivos']
        disciplina.ementas.append(ementa)
        return jsonify(disciplina)

    def show_disciplina(self, id):
        disciplina: Disciplina = DisciplinaService.get_disc_by_id(id)

        if disciplina is None:
            output = {"error": {"msg": "500 error: Disciplina não encontrada."}}
            resp = jsonify({'result': output})
            resp.status_code = 500
            return resp

        return jsonify(disciplina.to_dict())

    def update_disciplina(self, id):
        data = request.get_json()
        # atualizar a disciplina

    def nova_ementa(self, id):
        data = request.get_json()

    def update_ementa(self, id):
        data = request.get_json()
