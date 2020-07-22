from mongoengine import EmbeddedDocument, Document, StringField, ListField, SortedListField, DateTimeField, IntField, \
    ReferenceField, EmbeddedDocumentField

from src.models.Curso import Curso
from src.models.Disciplina import Disciplina
from src.models.User import User


class Aula(EmbeddedDocument):
    data = DateTimeField()
    titulo = StringField()
    objetivos = ListField(IntField())
    competencias = ListField(IntField())
    estrategia = StringField()


class PlanoAula(Document):
    proferssor = ReferenceField(User)
    disciplina = ReferenceField(Disciplina)
    curso = ReferenceField(Curso)
    cod_turma= StringField
    cronograma = ListField(EmbeddedDocumentField(Aula))
