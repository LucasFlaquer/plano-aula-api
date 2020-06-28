import json

from mongoengine import *

from src.models.Disciplina import Disciplina
from src.models.User import User


class Curso(Document):
    nome = StringField(required=True)
    turno = StringField(max_length=1)
    coordenador = ReferenceField(User, default=None)
    publico = BooleanField(default=True)
    disciplinas = ListField(ReferenceField(Disciplina), default=[])

    #@property
    def json(self):
        if self.coordenador == None:
            coord = 'Nenhum coordenador cadastrado'
        else:
            coord = self.coordenador.name
        curso_dict = {
            "nome": self.nome,
            "turno": self.turno,
            "coordenador": coord,
            "disciplinas": self.disciplinas
        }
        return json.dumps(curso_dict)