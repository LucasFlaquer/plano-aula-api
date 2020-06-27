from mongoengine import *

from src.models.Disciplina import Disciplina
from src.models.User import User


class Curso(Document):
    nome = StringField(required=True)
    turno = StringField(max_length=1)
    coordenador = ReferenceField(User)
    publico = BooleanField(default=True)
    disciplinas = ListField(ReferenceField(Disciplina), default=[])

'''
    classe curso possui:
    nome
    turno
    coordenador do curso
    pupblico se o curso está público ou 
'''