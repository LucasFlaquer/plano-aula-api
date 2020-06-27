from mongoengine import *


# class CodTurno(EmbeddedDocument):
#     cod = StringField(required=True)
#     turno = StringField(max_length=1, required=True)
#from src.models.Curso import Curso


class Ementa(EmbeddedDocument):
    
    data = DateTimeField()
    ementa = StringField()
    conteudo = ListField(StringField())
    competencias = ListField(StringField())
    objetivos = ListField(StringField())


class Disciplina(Document):
    nome = StringField()
    carga_pratica = IntField()
    carga_teoria = IntField()
    #list_cursos = ListField(ReferenceField(Curso))
    #prof_nde = ReferenceField()
