from mongoengine import EmbeddedDocument, Document, StringField, ListField, SortedListField, DateTimeField, IntField, \
    ReferenceField, EmbeddedDocumentField

from src.models.User import User


class Aula(EmbeddedDocument):
    data = DateTimeField()
    titulo = StringField()
    objetivos = ListField(IntField())
    competencias = ListField(IntField())
    estrategia = StringField()


class PlanoAula(Document):
    proferssor = ReferenceField(User)
    disciplina = StringField()
    curso = StringField()
    ementa = StringField()
    conteudo = ListField(StringField())
    competencias = ListField(StringField())
    objetivos = ListField(StringField())
    cronograma = ListField(EmbeddedDocumentField(Aula))
